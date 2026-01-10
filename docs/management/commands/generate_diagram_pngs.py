"""
Management command to generate PNG exports for diagrams from their XML.

Usage:
    python manage.py generate_diagram_pngs
    python manage.py generate_diagram_pngs --force
"""

from django.core.management.base import BaseCommand
from docs.models import Diagram
import requests
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Generate PNG exports for diagrams from their diagram XML'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate PNGs even if they already exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        self.stdout.write(self.style.SUCCESS('Generating diagram PNG exports...'))

        # Get all diagrams with XML
        diagrams = Diagram.objects.exclude(diagram_xml='')

        if not force:
            # Only generate for diagrams without PNG exports
            diagrams = diagrams.filter(png_export='')

        count = 0
        for diagram in diagrams:
            try:
                # Use diagrams.net export API to generate PNG
                url = 'https://exp.diagrams.net/ImageServlet4'
                response = requests.post(url, data={
                    'format': 'png',
                    'xml': diagram.diagram_xml,
                    'scale': '2',  # 2x resolution for better quality
                    'bg': '#ffffff'  # White background
                }, timeout=30)

                if response.status_code == 200:
                    # Save PNG export
                    filename = f"{diagram.slug}.png"
                    diagram.png_export.save(filename, ContentFile(response.content), save=True)
                    self.stdout.write(f'  ✓ Generated PNG for: {diagram.title}')
                    count += 1
                else:
                    self.stdout.write(self.style.ERROR(f'  ✗ Failed for {diagram.title}: HTTP {response.status_code}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed for {diagram.title}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\nGenerated {count} diagram PNG exports'))
