"""
Management command to set up initial data for HuduGlue installation.

This command runs all necessary seed commands in the correct order:
1. Document templates (global)
2. Diagram templates (global)
3. Global Knowledge Base articles
4. Acme Corporation sample data (demo organization with full sample data)

Usage:
    python manage.py setup_initial_data
    python manage.py setup_initial_data --skip-demo  # Skip Acme Corp sample data
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Set up initial data for HuduGlue (templates + sample data)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-demo',
            action='store_true',
            help='Skip creating Acme Corporation demo data',
        )

    def handle(self, *args, **options):
        skip_demo = options.get('skip_demo', False)

        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('HuduGlue Initial Data Setup'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('')

        # Step 1: Create document templates
        self.stdout.write(self.style.SUCCESS('Step 1/4: Creating global document templates...'))
        try:
            call_command('seed_templates')
            self.stdout.write(self.style.SUCCESS('✓ Document templates created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create document templates: {str(e)}'))

        self.stdout.write('')

        # Step 2: Create diagram templates
        self.stdout.write(self.style.SUCCESS('Step 2/4: Creating global diagram templates...'))
        try:
            call_command('seed_diagram_templates')
            self.stdout.write(self.style.SUCCESS('✓ Diagram templates created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create diagram templates: {str(e)}'))

        self.stdout.write('')

        # Step 3: Generate diagram preview images
        self.stdout.write(self.style.SUCCESS('Step 3/4: Generating diagram preview images...'))
        try:
            call_command('generate_diagram_previews', '--force')
            self.stdout.write(self.style.SUCCESS('✓ Diagram preview images generated'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to generate diagram previews: {str(e)}'))

        self.stdout.write('')

        # Step 4: Create global KB articles
        self.stdout.write(self.style.SUCCESS('Step 4/4: Creating Global Knowledge Base articles...'))
        try:
            call_command('create_global_kb')
            self.stdout.write(self.style.SUCCESS('✓ Global KB articles created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to create Global KB: {str(e)}'))

        self.stdout.write('')

        # Step 5: Create Acme Corporation demo data (optional)
        if not skip_demo:
            self.stdout.write(self.style.SUCCESS('Step 5/5: Creating Acme Corporation sample data...'))
            try:
                call_command('seed_demo_data')
                self.stdout.write(self.style.SUCCESS('✓ Acme Corporation sample data created'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to create sample data: {str(e)}'))
            self.stdout.write('')
        else:
            self.stdout.write(self.style.WARNING('Step 5/5: Skipping Acme Corporation sample data (--skip-demo)'))
            self.stdout.write('')

        # Summary
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('Setup Complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('')
        self.stdout.write('Your HuduGlue installation now includes:')
        self.stdout.write('  - Global document templates (5)')
        self.stdout.write('  - Global diagram templates (5)')
        self.stdout.write('  - Global Knowledge Base articles (4)')
        if not skip_demo:
            self.stdout.write('  - Acme Corporation demo organization with:')
            self.stdout.write('    - Sample users (demo.admin, demo.editor, demo.viewer)')
            self.stdout.write('    - Sample assets (servers, network devices, workstations)')
            self.stdout.write('    - Sample documents')
            self.stdout.write('    - Sample passwords')
            self.stdout.write('    - Sample processes')
            self.stdout.write('    - Sample diagrams')
            self.stdout.write('    - Sample contacts')
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Demo user password: demo123'))
        self.stdout.write('')
        self.stdout.write('You can delete the Acme Corporation organization at any time.')
        self.stdout.write('')
