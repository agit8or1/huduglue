"""
Security-related views - Package scanning, vulnerability monitoring
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.management import call_command
from django.utils import timezone
from .models import SystemPackageScan
import io
import json


@login_required
def package_scanner_dashboard(request):
    """
    Package scanner dashboard showing scan history and security status.
    Staff/superuser only.
    """
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "You don't have permission to access this feature.")
        return redirect('core:dashboard')

    # Get latest scan
    latest_scan = SystemPackageScan.objects.first()

    # Get scan history (last 30 scans)
    scan_history = SystemPackageScan.objects.all()[:30]

    # Calculate statistics
    stats = {
        'latest_scan_date': latest_scan.scan_date if latest_scan else None,
        'security_updates': latest_scan.security_updates if latest_scan else 0,
        'total_updates': latest_scan.upgradeable_packages if latest_scan else 0,
        'total_packages': latest_scan.total_packages if latest_scan else 0,
        'security_status': latest_scan.security_status if latest_scan else ('secondary', 'No scans yet'),
        'scan_count': scan_history.count(),
    }

    # Get trend data (last 7 scans)
    trend_scans = list(scan_history[:7])
    trend_scans.reverse()  # Oldest to newest

    trend_data = {
        'dates': [scan.scan_date.strftime('%m/%d') for scan in trend_scans],
        'security_updates': [scan.security_updates for scan in trend_scans],
        'total_updates': [scan.upgradeable_packages for scan in trend_scans],
    }

    return render(request, 'core/package_scanner_dashboard.html', {
        'latest_scan': latest_scan,
        'scan_history': scan_history,
        'stats': stats,
        'trend_data': trend_data,
    })


@login_required
@require_http_methods(["POST"])
def run_package_scan(request):
    """Run a package scan manually via web interface"""
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        # First, try to update the apt cache for latest data
        import subprocess
        cache_updated = False
        try:
            result = subprocess.run(
                ['sudo', '-n', 'apt-get', 'update'],
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode == 0:
                cache_updated = True
        except:
            pass  # Continue without cache update if it fails

        # Run scan command
        out = io.StringIO()
        call_command('scan_system_packages', '--save', '--json', stdout=out)

        # Parse output
        output = out.getvalue()
        scan_data = {}

        try:
            # Try direct JSON parse first
            scan_data = json.loads(output)
        except json.JSONDecodeError as e:
            # Command might have printed non-JSON info, find the JSON part
            lines = output.strip().split('\n')
            json_found = False

            for line in lines:
                line = line.strip()
                if line.startswith('{'):
                    try:
                        scan_data = json.loads(line)
                        json_found = True
                        break
                    except json.JSONDecodeError:
                        # Try to find JSON in multi-line output
                        try:
                            json_start_idx = output.index('{')
                            json_end_idx = output.rindex('}') + 1
                            json_str = output[json_start_idx:json_end_idx]
                            scan_data = json.loads(json_str)
                            json_found = True
                            break
                        except (ValueError, json.JSONDecodeError):
                            continue

            if not json_found:
                # If no JSON found, return error with diagnostic info
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to parse scan output: {str(e)}',
                    'raw_output': output[:500]  # First 500 chars for debugging
                }, status=500)

        # Add cache update status to scan data
        scan_data['cache_updated'] = cache_updated

        return JsonResponse({
            'success': True,
            'message': 'Scan completed successfully' + (' (cache updated)' if cache_updated else ' (using cached data)'),
            'cache_updated': cache_updated,
            'scan_data': scan_data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Scan failed: {str(e)}'
        }, status=500)


@login_required
@require_http_methods(["POST"])
def update_packages(request):
    """Update system packages via web interface (OPTIONAL)"""
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        security_only = request.POST.get('security_only') == 'true'
        packages = request.POST.get('packages', '')
        dry_run = request.POST.get('dry_run') == 'true'

        # Build command arguments
        args = ['--auto-approve']

        if security_only:
            args.append('--security-only')

        if packages:
            args.extend(['--package', packages])

        if dry_run:
            args.append('--dry-run')

        # Run update command
        out = io.StringIO()
        call_command('update_system_packages', *args, stdout=out)

        output = out.getvalue()

        return JsonResponse({
            'success': True,
            'message': 'Update completed successfully' if not dry_run else 'Dry run completed',
            'output': output
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def scan_detail(request, pk):
    """View details of a specific scan"""
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "You don't have permission to access this feature.")
        return redirect('core:dashboard')

    from django.shortcuts import get_object_or_404
    scan = get_object_or_404(SystemPackageScan, pk=pk)

    return render(request, 'core/package_scan_detail.html', {
        'scan': scan,
    })


@login_required
def get_dashboard_widget_data(request):
    """
    API endpoint to get package scanner data for dashboard widget.
    Returns JSON with security status.
    """
    if not (request.user.is_superuser or request.user.is_staff):
        return JsonResponse({'error': 'Permission denied'}, status=403)

    latest_scan = SystemPackageScan.objects.first()

    if not latest_scan:
        return JsonResponse({
            'status': 'no_data',
            'message': 'No scans available',
            'security_updates': 0,
            'total_updates': 0,
        })

    status_class, status_label = latest_scan.security_status

    return JsonResponse({
        'status': status_class,
        'status_label': status_label,
        'security_updates': latest_scan.security_updates,
        'total_updates': latest_scan.upgradeable_packages,
        'total_packages': latest_scan.total_packages,
        'scan_date': latest_scan.scan_date.isoformat(),
        'package_manager': latest_scan.package_manager,
    })
