"""
Views for Reports and Analytics
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse, JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    Dashboard, DashboardWidget, ReportTemplate, GeneratedReport,
    ScheduledReport, AnalyticsEvent
)
from .generators import REPORT_GENERATORS
import json


@login_required
def reports_home(request):
    """Reports and Analytics home page"""
    org = request.user.organization

    context = {
        'recent_reports': GeneratedReport.objects.filter(
            organization=org
        ).select_related('template', 'generated_by')[:10],
        'active_schedules': ScheduledReport.objects.filter(
            organization=org,
            is_active=True
        ).count(),
        'total_dashboards': Dashboard.objects.filter(
            Q(organization=org) | Q(is_global=True)
        ).count(),
        'templates_count': ReportTemplate.objects.filter(
            Q(organization=org) | Q(is_global=True)
        ).count(),
    }

    return render(request, 'reports/home.html', context)


@login_required
def dashboard_list(request):
    """List all available dashboards"""
    org = request.user.organization

    dashboards = Dashboard.objects.filter(
        Q(organization=org) | Q(is_global=True)
    ).prefetch_related('widgets')

    context = {
        'dashboards': dashboards,
    }

    return render(request, 'reports/dashboard_list.html', context)


@login_required
def dashboard_detail(request, pk):
    """View a specific dashboard"""
    org = request.user.organization

    dashboard = get_object_or_404(
        Dashboard,
        pk=pk,
        organization__in=[org, None]  # User's org or global
    )

    widgets = dashboard.widgets.all().order_by('position')

    context = {
        'dashboard': dashboard,
        'widgets': widgets,
    }

    return render(request, 'reports/dashboard_detail.html', context)


@login_required
def dashboard_create(request):
    """Create a new dashboard"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_default = request.POST.get('is_default') == 'on'

        dashboard = Dashboard.objects.create(
            name=name,
            description=description,
            is_default=is_default,
            organization=request.user.organization,
            created_by=request.user
        )

        messages.success(request, f'Dashboard "{name}" created successfully.')
        return redirect('reports:dashboard_detail', pk=dashboard.pk)

    return render(request, 'reports/dashboard_form.html', {'action': 'Create'})


@login_required
def dashboard_edit(request, pk):
    """Edit an existing dashboard"""
    dashboard = get_object_or_404(
        Dashboard,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        dashboard.name = request.POST.get('name')
        dashboard.description = request.POST.get('description', '')
        dashboard.is_default = request.POST.get('is_default') == 'on'
        dashboard.save()

        messages.success(request, f'Dashboard "{dashboard.name}" updated successfully.')
        return redirect('reports:dashboard_detail', pk=dashboard.pk)

    context = {
        'dashboard': dashboard,
        'action': 'Edit'
    }

    return render(request, 'reports/dashboard_form.html', context)


@login_required
def dashboard_delete(request, pk):
    """Delete a dashboard"""
    dashboard = get_object_or_404(
        Dashboard,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        name = dashboard.name
        dashboard.delete()
        messages.success(request, f'Dashboard "{name}" deleted successfully.')
        return redirect('reports:dashboard_list')

    context = {'dashboard': dashboard}
    return render(request, 'reports/dashboard_confirm_delete.html', context)


@login_required
def template_list(request):
    """List all report templates"""
    org = request.user.organization

    templates = ReportTemplate.objects.filter(
        Q(organization=org) | Q(is_global=True)
    ).select_related('created_by')

    # Group by report type
    templates_by_type = {}
    for template in templates:
        report_type = template.get_report_type_display()
        if report_type not in templates_by_type:
            templates_by_type[report_type] = []
        templates_by_type[report_type].append(template)

    context = {
        'templates': templates,
        'templates_by_type': templates_by_type,
    }

    return render(request, 'reports/template_list.html', context)


@login_required
def template_detail(request, pk):
    """View a report template"""
    org = request.user.organization

    template = get_object_or_404(
        ReportTemplate,
        pk=pk,
        organization__in=[org, None]
    )

    recent_reports = GeneratedReport.objects.filter(
        template=template,
        organization=org
    )[:10]

    context = {
        'template': template,
        'recent_reports': recent_reports,
    }

    return render(request, 'reports/template_detail.html', context)


@login_required
def template_create(request):
    """Create a new report template"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        report_type = request.POST.get('report_type')
        query_template = request.POST.get('query_template', '')
        is_global = request.POST.get('is_global') == 'on' and request.user.is_staff

        template = ReportTemplate.objects.create(
            name=name,
            description=description,
            report_type=report_type,
            query_template=query_template,
            is_global=is_global,
            organization=request.user.organization,
            created_by=request.user
        )

        messages.success(request, f'Report template "{name}" created successfully.')
        return redirect('reports:template_detail', pk=template.pk)

    context = {
        'action': 'Create',
        'report_types': ReportTemplate.REPORT_TYPES,
    }

    return render(request, 'reports/template_form.html', context)


@login_required
def template_edit(request, pk):
    """Edit a report template"""
    template = get_object_or_404(
        ReportTemplate,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        template.name = request.POST.get('name')
        template.description = request.POST.get('description', '')
        template.report_type = request.POST.get('report_type')
        template.query_template = request.POST.get('query_template', '')
        template.is_global = request.POST.get('is_global') == 'on' and request.user.is_staff
        template.save()

        messages.success(request, f'Report template "{template.name}" updated successfully.')
        return redirect('reports:template_detail', pk=template.pk)

    context = {
        'template': template,
        'action': 'Edit',
        'report_types': ReportTemplate.REPORT_TYPES,
    }

    return render(request, 'reports/template_form.html', context)


@login_required
def template_delete(request, pk):
    """Delete a report template"""
    template = get_object_or_404(
        ReportTemplate,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        name = template.name
        template.delete()
        messages.success(request, f'Report template "{name}" deleted successfully.')
        return redirect('reports:template_list')

    context = {'template': template}
    return render(request, 'reports/template_confirm_delete.html', context)


@login_required
def generate_report(request, pk):
    """Generate a report from a template"""
    org = request.user.organization

    template = get_object_or_404(
        ReportTemplate,
        pk=pk,
        organization__in=[org, None]
    )

    if request.method == 'POST':
        report_format = request.POST.get('format', 'pdf')
        parameters = {}

        # Create the report generation task
        report = GeneratedReport.objects.create(
            template=template,
            organization=org,
            generated_by=request.user,
            format=report_format,
            parameters=parameters,
            status='pending'
        )

        # In a real implementation, this would trigger a Celery task
        # For now, we'll mark it as completed immediately
        from .generators import REPORT_GENERATORS

        try:
            generator_class = REPORT_GENERATORS.get(template.report_type)
            if generator_class:
                generator = generator_class(org)
                data = generator.generate()

                # Store the data (in production, would generate actual file)
                report.status = 'completed'
                report.completed_at = timezone.now()
                report.save()

                messages.success(request, f'Report "{template.name}" generated successfully.')
            else:
                report.status = 'failed'
                report.error_message = 'No generator found for this report type'
                report.save()
                messages.error(request, 'Failed to generate report: No generator found.')
        except Exception as e:
            report.status = 'failed'
            report.error_message = str(e)
            report.save()
            messages.error(request, f'Failed to generate report: {str(e)}')

        return redirect('reports:generated_detail', pk=report.pk)

    context = {
        'template': template,
        'formats': GeneratedReport.FORMAT_CHOICES,
    }

    return render(request, 'reports/generate_form.html', context)


@login_required
def generated_list(request):
    """List all generated reports"""
    org = request.user.organization

    reports = GeneratedReport.objects.filter(
        organization=org
    ).select_related('template', 'generated_by').order_by('-created_at')

    context = {
        'reports': reports,
    }

    return render(request, 'reports/generated_list.html', context)


@login_required
def generated_detail(request, pk):
    """View a generated report"""
    report = get_object_or_404(
        GeneratedReport,
        pk=pk,
        organization=request.user.organization
    )

    context = {
        'report': report,
    }

    return render(request, 'reports/generated_detail.html', context)


@login_required
def generated_download(request, pk):
    """Download a generated report"""
    report = get_object_or_404(
        GeneratedReport,
        pk=pk,
        organization=request.user.organization
    )

    if report.file:
        return FileResponse(report.file.open('rb'), as_attachment=True)
    else:
        messages.error(request, 'Report file not found.')
        return redirect('reports:generated_detail', pk=pk)


@login_required
def generated_delete(request, pk):
    """Delete a generated report"""
    report = get_object_or_404(
        GeneratedReport,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Report deleted successfully.')
        return redirect('reports:generated_list')

    context = {'report': report}
    return render(request, 'reports/generated_confirm_delete.html', context)


@login_required
def scheduled_list(request):
    """List all scheduled reports"""
    org = request.user.organization

    schedules = ScheduledReport.objects.filter(
        organization=org
    ).select_related('template', 'created_by').order_by('next_run')

    context = {
        'schedules': schedules,
    }

    return render(request, 'reports/scheduled_list.html', context)


@login_required
def scheduled_create(request):
    """Create a new scheduled report"""
    org = request.user.organization

    if request.method == 'POST':
        name = request.POST.get('name')
        template_id = request.POST.get('template')
        frequency = request.POST.get('frequency')
        delivery_method = request.POST.get('delivery_method')
        recipients_str = request.POST.get('recipients', '')

        template = get_object_or_404(ReportTemplate, pk=template_id)
        recipients = [email.strip() for email in recipients_str.split(',') if email.strip()]

        # Calculate next run based on frequency
        next_run = timezone.now()
        if frequency == 'daily':
            next_run += timedelta(days=1)
        elif frequency == 'weekly':
            next_run += timedelta(weeks=1)
        elif frequency == 'monthly':
            next_run += timedelta(days=30)
        elif frequency == 'quarterly':
            next_run += timedelta(days=90)

        schedule = ScheduledReport.objects.create(
            name=name,
            template=template,
            organization=org,
            frequency=frequency,
            delivery_method=delivery_method,
            recipients=recipients,
            next_run=next_run,
            created_by=request.user
        )

        messages.success(request, f'Scheduled report "{name}" created successfully.')
        return redirect('reports:scheduled_list')

    templates = ReportTemplate.objects.filter(
        Q(organization=org) | Q(is_global=True)
    )

    context = {
        'action': 'Create',
        'templates': templates,
        'frequencies': ScheduledReport.FREQUENCY_CHOICES,
        'delivery_methods': ScheduledReport.DELIVERY_CHOICES,
    }

    return render(request, 'reports/scheduled_form.html', context)


@login_required
def scheduled_edit(request, pk):
    """Edit a scheduled report"""
    schedule = get_object_or_404(
        ScheduledReport,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        schedule.name = request.POST.get('name')
        template_id = request.POST.get('template')
        schedule.template = get_object_or_404(ReportTemplate, pk=template_id)
        schedule.frequency = request.POST.get('frequency')
        schedule.delivery_method = request.POST.get('delivery_method')
        recipients_str = request.POST.get('recipients', '')
        schedule.recipients = [email.strip() for email in recipients_str.split(',') if email.strip()]
        schedule.save()

        messages.success(request, f'Scheduled report "{schedule.name}" updated successfully.')
        return redirect('reports:scheduled_list')

    templates = ReportTemplate.objects.filter(
        Q(organization=schedule.organization) | Q(is_global=True)
    )

    context = {
        'schedule': schedule,
        'action': 'Edit',
        'templates': templates,
        'frequencies': ScheduledReport.FREQUENCY_CHOICES,
        'delivery_methods': ScheduledReport.DELIVERY_CHOICES,
        'recipients_str': ', '.join(schedule.recipients),
    }

    return render(request, 'reports/scheduled_form.html', context)


@login_required
def scheduled_delete(request, pk):
    """Delete a scheduled report"""
    schedule = get_object_or_404(
        ScheduledReport,
        pk=pk,
        organization=request.user.organization
    )

    if request.method == 'POST':
        name = schedule.name
        schedule.delete()
        messages.success(request, f'Scheduled report "{name}" deleted successfully.')
        return redirect('reports:scheduled_list')

    context = {'schedule': schedule}
    return render(request, 'reports/scheduled_confirm_delete.html', context)


@login_required
def scheduled_toggle(request, pk):
    """Toggle a scheduled report active/inactive"""
    schedule = get_object_or_404(
        ScheduledReport,
        pk=pk,
        organization=request.user.organization
    )

    schedule.is_active = not schedule.is_active
    schedule.save()

    status = 'enabled' if schedule.is_active else 'disabled'
    messages.success(request, f'Scheduled report "{schedule.name}" {status}.')

    return redirect('reports:scheduled_list')


@login_required
def analytics_overview(request):
    """Analytics overview dashboard"""
    org = request.user.organization

    # Get recent events
    recent_events = AnalyticsEvent.objects.filter(
        organization=org
    ).select_related('user')[:100]

    # Event counts by category
    events_by_category = AnalyticsEvent.objects.filter(
        organization=org,
        timestamp__gte=timezone.now() - timedelta(days=30)
    ).values('event_category').annotate(count=Count('id'))

    # Most active users
    active_users = AnalyticsEvent.objects.filter(
        organization=org,
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).values('user__username').annotate(count=Count('id')).order_by('-count')[:10]

    context = {
        'recent_events': recent_events,
        'events_by_category': events_by_category,
        'active_users': active_users,
    }

    return render(request, 'reports/analytics_overview.html', context)


@login_required
def analytics_events(request):
    """Detailed analytics events list"""
    org = request.user.organization

    events = AnalyticsEvent.objects.filter(
        organization=org
    ).select_related('user').order_by('-timestamp')

    # Apply filters
    category = request.GET.get('category')
    if category:
        events = events.filter(event_category=category)

    event_name = request.GET.get('event')
    if event_name:
        events = events.filter(event_name__icontains=event_name)

    # Pagination
    events = events[:500]  # Limit to 500 most recent

    context = {
        'events': events,
        'categories': AnalyticsEvent.CATEGORY_CHOICES,
    }

    return render(request, 'reports/analytics_events.html', context)
