"""
Firewall management views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from core.models import FirewallSettings, FirewallIPRule, FirewallCountryRule, FirewallLog
import logging

logger = logging.getLogger('core')


def is_superuser(user):
    """Check if user is a superuser."""
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def firewall_settings(request):
    """Firewall settings and rules management."""
    settings = FirewallSettings.get_settings()

    if request.method == 'POST':
        # Update settings
        settings.ip_firewall_enabled = request.POST.get('ip_firewall_enabled') == 'on'
        settings.ip_firewall_mode = request.POST.get('ip_firewall_mode', 'blocklist')
        settings.geoip_firewall_enabled = request.POST.get('geoip_firewall_enabled') == 'on'
        settings.geoip_firewall_mode = request.POST.get('geoip_firewall_mode', 'blocklist')
        settings.bypass_for_staff = request.POST.get('bypass_for_staff') == 'on'
        settings.bypass_for_api = request.POST.get('bypass_for_api') == 'on'
        settings.log_blocked_requests = request.POST.get('log_blocked_requests') == 'on'
        settings.updated_by = request.user
        settings.save()

        messages.success(request, 'Firewall settings updated successfully.')
        return redirect('core:firewall_settings')

    # Get rules and logs
    ip_rules = FirewallIPRule.objects.all()
    country_rules = FirewallCountryRule.objects.all()
    recent_blocks = FirewallLog.objects.all()[:20]

    # Get statistics
    total_blocks_today = FirewallLog.objects.filter(
        timestamp__gte=timezone.now() - timedelta(days=1)
    ).count()

    from django.utils import timezone
    from datetime import timedelta

    context = {
        'settings': settings,
        'ip_rules': ip_rules,
        'country_rules': country_rules,
        'recent_blocks': recent_blocks,
        'total_blocks_today': total_blocks_today,
        'ip_rules_count': ip_rules.count(),
        'country_rules_count': country_rules.count(),
    }

    return render(request, 'core/firewall_settings.html', context)


@login_required
@user_passes_test(is_superuser)
def firewall_ip_rules(request):
    """Manage IP firewall rules."""
    if request.method == 'POST':
        # Add new IP rule
        ip_address = request.POST.get('ip_address', '').strip()
        description = request.POST.get('description', '').strip()

        if ip_address:
            try:
                FirewallIPRule.objects.create(
                    ip_address=ip_address,
                    description=description,
                    created_by=request.user
                )
                messages.success(request, f'IP rule added: {ip_address}')
            except Exception as e:
                messages.error(request, f'Error adding IP rule: {str(e)}')
        else:
            messages.error(request, 'IP address is required.')

        return redirect('core:firewall_ip_rules')

    rules = FirewallIPRule.objects.all()

    context = {
        'rules': rules,
    }

    return render(request, 'core/firewall_ip_rules.html', context)


@login_required
@user_passes_test(is_superuser)
@require_POST
def firewall_ip_rule_delete(request, pk):
    """Delete an IP firewall rule."""
    rule = get_object_or_404(FirewallIPRule, pk=pk)
    ip_address = rule.ip_address
    rule.delete()
    messages.success(request, f'IP rule deleted: {ip_address}')
    return redirect('core:firewall_ip_rules')


@login_required
@user_passes_test(is_superuser)
@require_POST
def firewall_ip_rule_toggle(request, pk):
    """Toggle an IP firewall rule active state."""
    rule = get_object_or_404(FirewallIPRule, pk=pk)
    rule.is_active = not rule.is_active
    rule.save()

    status = "enabled" if rule.is_active else "disabled"
    messages.success(request, f'IP rule {status}: {rule.ip_address}')
    return redirect('core:firewall_ip_rules')


@login_required
@user_passes_test(is_superuser)
def firewall_country_rules(request):
    """Manage country firewall rules."""
    if request.method == 'POST':
        # Add new country rule
        country_code = request.POST.get('country_code', '').strip().upper()
        country_name = request.POST.get('country_name', '').strip()

        if country_code and country_name:
            try:
                FirewallCountryRule.objects.create(
                    country_code=country_code,
                    country_name=country_name,
                    created_by=request.user
                )
                messages.success(request, f'Country rule added: {country_name} ({country_code})')
            except Exception as e:
                messages.error(request, f'Error adding country rule: {str(e)}')
        else:
            messages.error(request, 'Country code and name are required.')

        return redirect('core:firewall_country_rules')

    rules = FirewallCountryRule.objects.all()

    # Common countries for quick add
    common_countries = [
        ('US', 'United States'),
        ('GB', 'United Kingdom'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('DE', 'Germany'),
        ('FR', 'France'),
        ('CN', 'China'),
        ('RU', 'Russia'),
        ('IN', 'India'),
        ('BR', 'Brazil'),
    ]

    context = {
        'rules': rules,
        'common_countries': common_countries,
    }

    return render(request, 'core/firewall_country_rules.html', context)


@login_required
@user_passes_test(is_superuser)
@require_POST
def firewall_country_rule_delete(request, pk):
    """Delete a country firewall rule."""
    rule = get_object_or_404(FirewallCountryRule, pk=pk)
    country_name = rule.country_name
    rule.delete()
    messages.success(request, f'Country rule deleted: {country_name}')
    return redirect('core:firewall_country_rules')


@login_required
@user_passes_test(is_superuser)
@require_POST
def firewall_country_rule_toggle(request, pk):
    """Toggle a country firewall rule active state."""
    rule = get_object_or_404(FirewallCountryRule, pk=pk)
    rule.is_active = not rule.is_active
    rule.save()

    status = "enabled" if rule.is_active else "disabled"
    messages.success(request, f'Country rule {status}: {rule.country_name}')
    return redirect('core:firewall_country_rules')


@login_required
@user_passes_test(is_superuser)
def firewall_logs(request):
    """View firewall logs."""
    logs_list = FirewallLog.objects.select_related('user').all()

    # Pagination
    paginator = Paginator(logs_list, 50)  # 50 logs per page
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)

    # Statistics
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count

    total_blocks = FirewallLog.objects.count()
    blocks_today = FirewallLog.objects.filter(
        timestamp__gte=timezone.now() - timedelta(days=1)
    ).count()
    blocks_this_week = FirewallLog.objects.filter(
        timestamp__gte=timezone.now() - timedelta(days=7)
    ).count()

    # Top blocked IPs
    top_ips = FirewallLog.objects.values('ip_address').annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    # Top blocked countries
    top_countries = FirewallLog.objects.exclude(country_code='').values(
        'country_code', 'country_name'
    ).annotate(
        count=Count('id')
    ).order_by('-count')[:10]

    context = {
        'logs': logs,
        'total_blocks': total_blocks,
        'blocks_today': blocks_today,
        'blocks_this_week': blocks_this_week,
        'top_ips': top_ips,
        'top_countries': top_countries,
    }

    return render(request, 'core/firewall_logs.html', context)


@login_required
@user_passes_test(is_superuser)
@require_POST
def firewall_logs_clear(request):
    """Clear all firewall logs."""
    count = FirewallLog.objects.count()
    FirewallLog.objects.all().delete()
    messages.success(request, f'Cleared {count} firewall log entries.')
    return redirect('core:firewall_logs')
