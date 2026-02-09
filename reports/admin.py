"""
Django Admin Configuration for Reports and Analytics
"""
from django.contrib import admin
from .models import (
    Dashboard, DashboardWidget, ReportTemplate, GeneratedReport,
    ScheduledReport, AnalyticsEvent
)


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'is_default', 'is_global', 'created_by', 'created_at')
    list_filter = ('is_default', 'is_global', 'created_at', 'organization')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'organization', 'created_by')
        }),
        ('Settings', {
            'fields': ('is_default', 'is_global', 'layout')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('title', 'dashboard', 'widget_type', 'data_source', 'refresh_interval')
    list_filter = ('widget_type', 'dashboard')
    search_fields = ('title', 'data_source')
    readonly_fields = ('created_at',)


@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'organization', 'is_global', 'created_by', 'created_at')
    list_filter = ('report_type', 'is_global', 'created_at', 'organization')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'report_type')
        }),
        ('Configuration', {
            'fields': ('query_template', 'parameters', 'organization', 'is_global')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(GeneratedReport)
class GeneratedReportAdmin(admin.ModelAdmin):
    list_display = ('template', 'organization', 'generated_by', 'status', 'format', 'created_at', 'completed_at')
    list_filter = ('status', 'format', 'created_at', 'organization')
    search_fields = ('template__name',)
    readonly_fields = ('created_at', 'completed_at', 'generation_time', 'file_size')

    fieldsets = (
        ('Report Information', {
            'fields': ('template', 'organization', 'generated_by', 'scheduled_report')
        }),
        ('Status', {
            'fields': ('status', 'error_message')
        }),
        ('Output', {
            'fields': ('format', 'file', 'file_size', 'parameters')
        }),
        ('Timing', {
            'fields': ('created_at', 'completed_at', 'generation_time')
        }),
    )


@admin.register(ScheduledReport)
class ScheduledReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'template', 'organization', 'frequency', 'is_active', 'next_run', 'last_run')
    list_filter = ('frequency', 'is_active', 'delivery_method', 'organization')
    search_fields = ('name', 'template__name')
    readonly_fields = ('created_at', 'last_run')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'template', 'organization', 'created_by')
        }),
        ('Schedule', {
            'fields': ('frequency', 'is_active', 'next_run', 'last_run')
        }),
        ('Delivery', {
            'fields': ('delivery_method', 'recipients')
        }),
        ('Parameters', {
            'fields': ('parameters',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'event_category', 'user', 'organization', 'ip_address', 'timestamp')
    list_filter = ('event_category', 'timestamp', 'organization')
    search_fields = ('event_name', 'user__username', 'ip_address')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Event Information', {
            'fields': ('event_name', 'event_category', 'metadata')
        }),
        ('Context', {
            'fields': ('user', 'organization', 'ip_address', 'user_agent')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )

    # Make it read-only in admin (events shouldn't be edited)
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
