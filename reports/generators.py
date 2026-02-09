"""
Report Generators for different report types
"""

from datetime import datetime, timedelta
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone

from assets.models import Asset
from vault.models import Password
from docs.models import Document
from monitoring.models import WebsiteMonitor, Expiration


class ReportGenerator:
    """Base report generator class"""

    def __init__(self, organization, parameters=None):
        self.organization = organization
        self.parameters = parameters or {}

    def generate(self):
        """Override in subclasses"""
        raise NotImplementedError


class AssetSummaryReport(ReportGenerator):
    """Asset summary report"""

    def generate(self):
        assets = Asset.objects.filter(organization=self.organization)

        # Asset counts by type
        by_type = assets.values('asset_type__name').annotate(
            count=Count('id')
        ).order_by('-count')

        # Asset counts by status
        active_count = assets.filter(is_active=True).count()
        inactive_count = assets.filter(is_active=False).count()

        # Recently added
        days = self.parameters.get('recent_days', 30)
        recent_date = timezone.now() - timedelta(days=days)
        recent_assets = assets.filter(created_at__gte=recent_date).count()

        return {
            'total_assets': assets.count(),
            'active_assets': active_count,
            'inactive_assets': inactive_count,
            'recent_assets': recent_assets,
            'by_type': list(by_type),
            'generated_at': datetime.now().isoformat(),
        }


class AssetLifecycleReport(ReportGenerator):
    """Asset lifecycle and age analysis"""

    def generate(self):
        assets = Asset.objects.filter(organization=self.organization)

        # Age distribution
        now = timezone.now()
        age_ranges = {
            '0-1 years': 0,
            '1-3 years': 0,
            '3-5 years': 0,
            '5+ years': 0,
        }

        for asset in assets:
            if asset.created_at:
                age_days = (now - asset.created_at).days
                age_years = age_days / 365

                if age_years < 1:
                    age_ranges['0-1 years'] += 1
                elif age_years < 3:
                    age_ranges['1-3 years'] += 1
                elif age_years < 5:
                    age_ranges['3-5 years'] += 1
                else:
                    age_ranges['5+ years'] += 1

        return {
            'total_assets': assets.count(),
            'age_distribution': age_ranges,
            'generated_at': datetime.now().isoformat(),
        }


class PasswordAuditReport(ReportGenerator):
    """Password security audit"""

    def generate(self):
        passwords = Password.objects.filter(organization=self.organization)

        # Passwords with weak indicators
        no_special_chars = 0
        short_passwords = 0
        old_passwords = 0

        # TOTP enabled count
        totp_enabled = passwords.exclude(totp_secret='').count()

        # Recently changed
        days = self.parameters.get('recent_days', 90)
        recent_date = timezone.now() - timedelta(days=days)
        recently_updated = passwords.filter(updated_at__gte=recent_date).count()

        # Passwords by category
        by_category = passwords.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'total_passwords': passwords.count(),
            'totp_enabled': totp_enabled,
            'totp_percentage': round((totp_enabled / passwords.count() * 100) if passwords.count() > 0 else 0, 2),
            'recently_updated': recently_updated,
            'by_category': list(by_category),
            'generated_at': datetime.now().isoformat(),
        }


class DocumentUsageReport(ReportGenerator):
    """Document usage and access patterns"""

    def generate(self):
        documents = Document.objects.filter(organization=self.organization)

        # Document counts
        total = documents.count()
        archived = documents.filter(is_archived=True).count()
        active = total - archived

        # By category
        by_category = documents.values('category__name').annotate(
            count=Count('id')
        ).order_by('-count')

        # By content type
        by_type = documents.values('content_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Recently created
        days = self.parameters.get('recent_days', 30)
        recent_date = timezone.now() - timedelta(days=days)
        recent_docs = documents.filter(created_at__gte=recent_date).count()

        return {
            'total_documents': total,
            'active_documents': active,
            'archived_documents': archived,
            'recent_documents': recent_docs,
            'by_category': list(by_category),
            'by_type': list(by_type),
            'generated_at': datetime.now().isoformat(),
        }


class MonitorUptimeReport(ReportGenerator):
    """Website monitor uptime report"""

    def generate(self):
        monitors = WebsiteMonitor.objects.filter(organization=self.organization)

        # Status counts
        up_count = monitors.filter(status='up').count()
        down_count = monitors.filter(status='down').count()
        warning_count = monitors.filter(status='warning').count()

        # Average response time (if stored)
        # This would require adding response time tracking to the model

        # By status
        by_status = monitors.values('status').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'total_monitors': monitors.count(),
            'up': up_count,
            'down': down_count,
            'warning': warning_count,
            'uptime_percentage': round((up_count / monitors.count() * 100) if monitors.count() > 0 else 0, 2),
            'by_status': list(by_status),
            'generated_at': datetime.now().isoformat(),
        }


class ExpirationForecastReport(ReportGenerator):
    """Expiration forecast report"""

    def generate(self):
        expirations = Expiration.objects.filter(organization=self.organization)

        now = timezone.now().date()

        # Expiring in different time frames
        forecast = {
            'expired': 0,
            'expiring_7_days': 0,
            'expiring_30_days': 0,
            'expiring_90_days': 0,
            'future': 0,
        }

        for exp in expirations:
            if exp.expiration_date:
                days_until = (exp.expiration_date - now).days

                if days_until < 0:
                    forecast['expired'] += 1
                elif days_until <= 7:
                    forecast['expiring_7_days'] += 1
                elif days_until <= 30:
                    forecast['expiring_30_days'] += 1
                elif days_until <= 90:
                    forecast['expiring_90_days'] += 1
                else:
                    forecast['future'] += 1

        # By type
        by_type = expirations.values('type').annotate(
            count=Count('id')
        ).order_by('-count')

        return {
            'total_expirations': expirations.count(),
            'forecast': forecast,
            'by_type': list(by_type),
            'generated_at': datetime.now().isoformat(),
        }


class OrganizationMetricsReport(ReportGenerator):
    """Overall organization metrics"""

    def generate(self):
        from accounts.models import OrganizationMember

        # Member counts
        members = OrganizationMember.objects.filter(organization=self.organization)
        member_count = members.count()
        active_members = members.filter(user__is_active=True).count()

        # Asset metrics
        assets = Asset.objects.filter(organization=self.organization)
        asset_count = assets.count()
        active_assets = assets.filter(is_active=True).count()

        # Password metrics
        password_count = Password.objects.filter(organization=self.organization).count()

        # Document metrics
        document_count = Document.objects.filter(organization=self.organization).count()

        # Monitor metrics
        monitor_count = WebsiteMonitor.objects.filter(organization=self.organization).count()

        return {
            'organization': {
                'name': self.organization.name,
                'member_count': member_count,
                'active_members': active_members,
            },
            'metrics': {
                'assets': {
                    'total': asset_count,
                    'active': active_assets,
                },
                'passwords': password_count,
                'documents': document_count,
                'monitors': monitor_count,
            },
            'generated_at': datetime.now().isoformat(),
        }


# Report generator registry
REPORT_GENERATORS = {
    'asset_summary': AssetSummaryReport,
    'asset_lifecycle': AssetLifecycleReport,
    'password_audit': PasswordAuditReport,
    'document_usage': DocumentUsageReport,
    'monitor_uptime': MonitorUptimeReport,
    'expiration_forecast': ExpirationForecastReport,
    'organization_metrics': OrganizationMetricsReport,
}


def get_report_generator(report_type):
    """Get report generator class by type"""
    return REPORT_GENERATORS.get(report_type)
