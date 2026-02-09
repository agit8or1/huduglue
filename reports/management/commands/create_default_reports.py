"""
Management command to create default report templates
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reports.models import ReportTemplate, Dashboard

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates default report templates and dashboards'

    def handle(self, *args, **options):
        self.stdout.write('Creating default report templates...')

        # Get or create a system user for created_by field
        system_user, _ = User.objects.get_or_create(
            username='system',
            defaults={
                'email': 'system@localhost',
                'is_active': False,
                'is_staff': False
            }
        )

        templates_created = 0
        dashboards_created = 0

        # Define default templates
        default_templates = [
            {
                'name': 'Asset Summary Report',
                'description': 'Comprehensive overview of all assets in your organization including counts by type, status, and location.',
                'report_type': 'asset_summary',
                'is_global': True
            },
            {
                'name': 'Asset Lifecycle Report',
                'description': 'Track asset age, warranty status, and planned replacements.',
                'report_type': 'asset_lifecycle',
                'is_global': True
            },
            {
                'name': 'Password Security Audit',
                'description': 'Analyze password age, complexity, and identify accounts that may need attention.',
                'report_type': 'password_audit',
                'is_global': True
            },
            {
                'name': 'Document Usage Report',
                'description': 'Track document creation, updates, and access patterns.',
                'report_type': 'document_usage',
                'is_global': True
            },
            {
                'name': 'Monitor Uptime Report',
                'description': 'Website and WAN connection uptime statistics and incident history.',
                'report_type': 'monitor_uptime',
                'is_global': True
            },
            {
                'name': 'Expiration Forecast',
                'description': 'View upcoming expirations for SSL certificates, domains, and credentials.',
                'report_type': 'expiration_forecast',
                'is_global': True
            },
            {
                'name': 'User Activity Report',
                'description': 'Track user logins, actions, and system usage patterns.',
                'report_type': 'user_activity',
                'is_global': True
            },
            {
                'name': 'Organization Metrics',
                'description': 'High-level metrics and KPIs for your organization.',
                'report_type': 'organization_metrics',
                'is_global': True
            }
        ]

        for template_data in default_templates:
            template, created = ReportTemplate.objects.get_or_create(
                name=template_data['name'],
                report_type=template_data['report_type'],
                defaults={
                    'description': template_data['description'],
                    'query_template': '',
                    'is_global': template_data['is_global'],
                    'created_by': system_user
                }
            )
            if created:
                templates_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ Created: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  - Already exists: {template.name}')
                )

        # Create default dashboard
        dashboard, created = Dashboard.objects.get_or_create(
            name='Executive Dashboard',
            defaults={
                'description': 'High-level overview of key metrics and system health',
                'is_global': True,
                'is_default': True,
                'created_by': system_user
            }
        )
        if created:
            dashboards_created += 1
            self.stdout.write(
                self.style.SUCCESS(f'  ✓ Created dashboard: {dashboard.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'  - Dashboard already exists: {dashboard.name}')
            )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Created {templates_created} report templates and {dashboards_created} dashboards.'
            )
        )
