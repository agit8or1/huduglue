"""
Reports and Analytics Models
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Organization

User = get_user_model()


class ReportTemplate(models.Model):
    """Pre-defined report templates"""

    REPORT_TYPES = [
        ('asset_summary', 'Asset Summary'),
        ('asset_lifecycle', 'Asset Lifecycle'),
        ('password_audit', 'Password Security Audit'),
        ('document_usage', 'Document Usage'),
        ('monitor_uptime', 'Monitor Uptime'),
        ('expiration_forecast', 'Expiration Forecast'),
        ('user_activity', 'User Activity'),
        ('organization_metrics', 'Organization Metrics'),
        ('custom', 'Custom Query'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    query_template = models.TextField(help_text='SQL or Django ORM query template')
    parameters = models.JSONField(default=dict, help_text='Report parameters schema')
    is_global = models.BooleanField(default=False, help_text='Available to all users')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='report_templates'
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class ScheduledReport(models.Model):
    """Scheduled report generation"""

    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]

    DELIVERY_METHODS = [
        ('email', 'Email'),
        ('download', 'Download Only'),
        ('both', 'Email and Download'),
    ]

    name = models.CharField(max_length=200)
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_METHODS, default='email')
    recipients = models.JSONField(default=list, help_text='List of email addresses')
    parameters = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['next_run']

    def __str__(self):
        return f"{self.name} - {self.get_frequency_display()}"


class GeneratedReport(models.Model):
    """Generated report instances"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('json', 'JSON'),
    ]

    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE)
    scheduled_report = models.ForeignKey(
        ScheduledReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    format = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='pdf')
    parameters = models.JSONField(default=dict)
    file = models.FileField(upload_to='reports/%Y/%m/', null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    generation_time = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.template.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Dashboard(models.Model):
    """Custom dashboards"""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_default = models.BooleanField(default=False)
    is_global = models.BooleanField(default=False)
    layout = models.JSONField(default=dict, help_text='Dashboard widget layout')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class DashboardWidget(models.Model):
    """Dashboard widgets"""

    WIDGET_TYPES = [
        ('metric', 'Metric Card'),
        ('chart_line', 'Line Chart'),
        ('chart_bar', 'Bar Chart'),
        ('chart_pie', 'Pie Chart'),
        ('table', 'Data Table'),
        ('list', 'List View'),
        ('calendar', 'Calendar'),
        ('map', 'Map'),
    ]

    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='widgets')
    title = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    data_source = models.CharField(max_length=100, help_text='Data source identifier')
    query_params = models.JSONField(default=dict)
    position = models.JSONField(default=dict, help_text='Grid position {x, y, width, height}')
    refresh_interval = models.IntegerField(
        default=300,
        help_text='Auto-refresh interval in seconds (0 = no auto-refresh)'
    )
    configuration = models.JSONField(default=dict, help_text='Widget-specific configuration')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['dashboard', 'position']

    def __str__(self):
        return f"{self.dashboard.name} - {self.title}"


class AnalyticsEvent(models.Model):
    """Track user and system events for analytics"""

    EVENT_CATEGORIES = [
        ('user', 'User Action'),
        ('system', 'System Event'),
        ('api', 'API Call'),
        ('security', 'Security Event'),
    ]

    event_name = models.CharField(max_length=100)
    event_category = models.CharField(max_length=20, choices=EVENT_CATEGORIES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_name', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['organization', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.event_name} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
