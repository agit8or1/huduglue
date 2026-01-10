"""
Management command to generate preview images for document templates.

Usage:
    python manage.py generate_document_previews
    python manage.py generate_document_previews --force
"""

from django.core.management.base import BaseCommand
from docs.models import Document
from docs.utils import generate_document_preview_image


class Command(BaseCommand):
    help = 'Generate preview images for document templates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate previews even if they already exist',
        )

    def handle(self, *args, **options):
        force = options.get('force', False)

        self.stdout.write(self.style.SUCCESS('Generating document template previews...'))

        # Get all document templates
        templates = Document.objects.filter(is_template=True)

        if not force:
            # Only generate for templates without previews
            templates = templates.filter(preview_image__isnull=True) | templates.filter(preview_image='')

        count = 0
        for template in templates:
            try:
                # Generate preview image
                buffer = generate_document_preview_image(template)

                # Save to template
                filename = f"{template.slug}_preview.png"
                from django.core.files.base import ContentFile
                template.preview_image.save(filename, ContentFile(buffer.read()), save=False)
                template.save()

                self.stdout.write(f'  ✓ Generated preview for: {template.title}')
                count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed for {template.title}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\nGenerated {count} document template previews'))
