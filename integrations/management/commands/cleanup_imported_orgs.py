"""
Django management command to clean up imported PSA/RMM organizations.
Usage: python manage.py cleanup_imported_orgs [--dry-run] [--psa] [--rmm]
"""
from django.core.management.base import BaseCommand
from django.db.models import Count, Q
from core.models import Organization
from integrations.models import PSAConnection, RMMConnection, ExternalObjectMap
from audit.models import AuditLog


class Command(BaseCommand):
    help = 'Clean up imported PSA/RMM organizations that have no other data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--psa',
            action='store_true',
            help='Only clean up PSA-imported organizations',
        )
        parser.add_argument(
            '--rmm',
            action='store_true',
            help='Only clean up RMM-imported organizations',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Delete organizations even if they have other data (use with caution!)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        psa_only = options['psa']
        rmm_only = options['rmm']
        force = options['force']

        self.stdout.write(self.style.HTTP_INFO('Organization Cleanup Tool'))
        self.stdout.write(self.style.HTTP_INFO('=' * 50))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No deletions will occur'))
            self.stdout.write('')

        total_deleted = 0

        # Clean up PSA imported organizations
        if not rmm_only:
            psa_deleted = self._cleanup_psa_orgs(dry_run, force)
            total_deleted += psa_deleted

        # Clean up RMM imported organizations
        if not psa_only:
            rmm_deleted = self._cleanup_rmm_orgs(dry_run, force)
            total_deleted += rmm_deleted

        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('=' * 50))
        if dry_run:
            self.stdout.write(self.style.WARNING(f'WOULD DELETE: {total_deleted} organizations'))
            self.stdout.write('Run without --dry-run to actually delete')
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ Deleted {total_deleted} organizations'))

    def _cleanup_psa_orgs(self, dry_run, force):
        """Clean up PSA-imported organizations."""
        self.stdout.write(self.style.HTTP_INFO('Scanning PSA-imported organizations...'))

        # Find all organizations tracked in ExternalObjectMap
        psa_mappings = ExternalObjectMap.objects.filter(
            local_type='organization'
        ).select_related('organization', 'connection')

        deleted_count = 0

        for mapping in psa_mappings:
            try:
                org = Organization.objects.get(id=mapping.local_id)
            except Organization.DoesNotExist:
                # Orphaned mapping
                self.stdout.write(f'  ⚠ Orphaned mapping for org ID {mapping.local_id}')
                if not dry_run:
                    mapping.delete()
                continue

            # Check if org has data besides PSA data
            has_data = (
                org.passwords.exists() or
                org.assets.exists() or
                org.documents.exists() or
                org.processes.exists() or
                org.website_monitors.exists()
            )

            psa_data_count = (
                org.psa_companies.count() +
                org.psa_contacts.count() +
                org.psa_tickets.count()
            )

            if has_data and not force:
                self.stdout.write(
                    f'  ⏭  Skipping "{org.name}" - has user data '
                    f'(passwords/assets/docs/etc)'
                )
                continue

            # This org is safe to delete (only has PSA data)
            self.stdout.write(
                f'  🗑  "{org.name}" - PSA data: {psa_data_count}, other data: {"yes" if has_data else "no"}'
            )

            if not dry_run:
                org.delete()

            deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'PSA: {"Would delete" if dry_run else "Deleted"} {deleted_count} organizations')
        )
        self.stdout.write('')

        return deleted_count

    def _cleanup_rmm_orgs(self, dry_run, force):
        """Clean up RMM-imported organizations."""
        self.stdout.write(self.style.HTTP_INFO('Scanning RMM-imported organizations...'))

        # Find organizations that have RMM devices
        orgs_with_rmm = Organization.objects.filter(
            rmm_devices__isnull=False
        ).distinct()

        deleted_count = 0

        for org in orgs_with_rmm:
            # Check if org has data besides RMM devices
            has_data = (
                org.passwords.exists() or
                org.assets.exists() or
                org.documents.exists() or
                org.processes.exists() or
                org.website_monitors.exists() or
                org.contacts.exists()
            )

            rmm_device_count = org.rmm_devices.count()

            if has_data and not force:
                self.stdout.write(
                    f'  ⏭  Skipping "{org.name}" - has user data '
                    f'(passwords/assets/docs/etc)'
                )
                continue

            # Check if this org has RMM prefix (more likely to be auto-imported)
            has_rmm_prefix = False
            for conn in RMMConnection.objects.all():
                if conn.org_name_prefix and org.name.startswith(conn.org_name_prefix):
                    has_rmm_prefix = True
                    break

            if not has_rmm_prefix and not force:
                self.stdout.write(
                    f'  ⏭  Skipping "{org.name}" - no RMM prefix '
                    f'(may be manually created)'
                )
                continue

            # This org is safe to delete (only has RMM devices)
            self.stdout.write(
                f'  🗑  "{org.name}" - RMM devices: {rmm_device_count}, other data: {"yes" if has_data else "no"}'
            )

            if not dry_run:
                org.delete()

            deleted_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'RMM: {"Would delete" if dry_run else "Deleted"} {deleted_count} organizations')
        )
        self.stdout.write('')

        return deleted_count
