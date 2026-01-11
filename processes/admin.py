"""
Processes admin configuration
"""
from django.contrib import admin
from .models import Process, ProcessStage, ProcessExecution, ProcessStageCompletion


class ProcessStageInline(admin.TabularInline):
    model = ProcessStage
    extra = 1
    fields = ['order', 'title', 'description', 'requires_confirmation', 'estimated_duration_minutes']
    ordering = ['order']


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'organization', 'is_published', 'is_template', 'is_global', 'created_by', 'created_at']
    list_filter = ['category', 'is_published', 'is_template', 'is_global', 'is_archived', 'organization', 'created_at']
    search_fields = ['title', 'slug', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['organization', 'created_by', 'last_modified_by', 'linked_diagram']
    filter_horizontal = ['tags']
    inlines = [ProcessStageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'organization')
        }),
        ('Categorization', {
            'fields': ('category', 'tags', 'linked_diagram')
        }),
        ('Status & Visibility', {
            'fields': ('is_published', 'is_template', 'is_global', 'is_archived')
        }),
        ('Metadata', {
            'fields': ('created_by', 'last_modified_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProcessStage)
class ProcessStageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order', 'process', 'requires_confirmation', 'estimated_duration_minutes']
    list_filter = ['requires_confirmation', 'process']
    search_fields = ['title', 'description', 'process__title']
    raw_id_fields = ['process', 'linked_document', 'linked_password', 'linked_secure_note', 'linked_asset']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['process', 'order']

    fieldsets = (
        ('Basic Information', {
            'fields': ('process', 'order', 'title', 'description')
        }),
        ('Configuration', {
            'fields': ('requires_confirmation', 'estimated_duration_minutes')
        }),
        ('Entity Links', {
            'fields': ('linked_document', 'linked_password', 'linked_secure_note', 'linked_asset'),
            'description': 'Link to one entity (document, password, secure note, or asset). Only one can be selected.'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class ProcessStageCompletionInline(admin.TabularInline):
    model = ProcessStageCompletion
    extra = 0
    fields = ['stage', 'is_completed', 'completed_by', 'completed_at', 'notes']
    readonly_fields = ['stage', 'completed_at']
    can_delete = False


@admin.register(ProcessExecution)
class ProcessExecutionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'process', 'assigned_to', 'status', 'started_at', 'completed_at', 'due_date', 'organization']
    list_filter = ['status', 'organization', 'created_at', 'started_at', 'completed_at']
    search_fields = ['process__title', 'assigned_to__username', 'started_by__username', 'notes']
    raw_id_fields = ['process', 'organization', 'assigned_to', 'started_by']
    readonly_fields = ['created_at', 'updated_at', 'completion_percentage', 'is_overdue']
    inlines = [ProcessStageCompletionInline]

    fieldsets = (
        ('Workflow Information', {
            'fields': ('process', 'organization')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'started_by')
        }),
        ('Status & Timing', {
            'fields': ('status', 'started_at', 'completed_at', 'due_date', 'completion_percentage', 'is_overdue')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProcessStageCompletion)
class ProcessStageCompletionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'execution', 'stage', 'is_completed', 'completed_by', 'completed_at']
    list_filter = ['is_completed', 'completed_at']
    search_fields = ['stage__title', 'execution__process__title', 'notes']
    raw_id_fields = ['execution', 'stage', 'completed_by']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']

    fieldsets = (
        ('Execution & Stage', {
            'fields': ('execution', 'stage')
        }),
        ('Completion Status', {
            'fields': ('is_completed', 'completed_by', 'completed_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
