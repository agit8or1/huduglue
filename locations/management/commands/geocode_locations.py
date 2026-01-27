"""
Management command to geocode locations that don't have coordinates.
"""
from django.core.management.base import BaseCommand
from locations.models import Location
from locations.services import get_geocoding_service
import logging

logger = logging.getLogger('locations')


class Command(BaseCommand):
    help = 'Geocode locations that are missing latitude/longitude coordinates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--organization',
            type=int,
            help='Only geocode locations for a specific organization ID',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Re-geocode all locations, even those with existing coordinates',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Maximum number of locations to geocode (default: 100)',
        )

    def handle(self, *args, **options):
        organization_id = options.get('organization')
        force = options.get('force')
        limit = options.get('limit')

        # Build query
        query = Location.objects.all()

        if organization_id:
            query = query.filter(organization_id=organization_id)
            self.stdout.write(f"Filtering to organization ID: {organization_id}")

        if not force:
            query = query.filter(latitude__isnull=True, longitude__isnull=True)
            self.stdout.write("Only geocoding locations without coordinates")
        else:
            self.stdout.write("Force mode: re-geocoding all locations")

        locations = query[:limit]
        total_count = locations.count()

        if total_count == 0:
            self.stdout.write(self.style.SUCCESS("No locations to geocode."))
            return

        self.stdout.write(f"\nGeocoding {total_count} location(s)...")

        geocoding_service = get_geocoding_service()
        success_count = 0
        fail_count = 0

        for location in locations:
            try:
                self.stdout.write(f"  Processing: {location.name} ({location.full_address})...")

                geo_data = geocoding_service.geocode_address(location.full_address)

                if geo_data:
                    location.latitude = geo_data['latitude']
                    location.longitude = geo_data['longitude']
                    if 'place_id' in geo_data:
                        location.google_place_id = geo_data.get('place_id', '')
                    location.save()

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"    ✓ Geocoded: {geo_data['latitude']}, {geo_data['longitude']}"
                        )
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"    ✗ Could not geocode address"
                        )
                    )
                    fail_count += 1

            except Exception as e:
                logger.error(f"Geocoding failed for location {location.id}: {e}")
                self.stdout.write(
                    self.style.ERROR(f"    ✗ Error: {str(e)}")
                )
                fail_count += 1

        # Summary
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"✓ Successfully geocoded: {success_count}"))
        if fail_count > 0:
            self.stdout.write(self.style.WARNING(f"✗ Failed: {fail_count}"))
        self.stdout.write("=" * 50)

        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nGeocoding complete! {success_count} location(s) now have coordinates and will appear on the map."
                )
            )
