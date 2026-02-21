"""
Integrated documentation and help system
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import markdown
import os


@login_required
def help_index(request):
    """Main help documentation index"""
    return render(request, 'core/help/index.html', {
        'title': 'Help & Documentation'
    })


@login_required
def help_getting_started(request):
    """Getting started guide"""
    return render(request, 'core/help/getting_started.html', {
        'title': 'Getting Started'
    })


@login_required
def help_features(request):
    """Features documentation"""
    # Read FEATURES.md and convert to HTML
    features_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'FEATURES.md')
    try:
        with open(features_path, 'r') as f:
            content = f.read()
            html_content = markdown.markdown(content, extensions=['tables', 'fenced_code', 'toc'])
    except:
        html_content = "<p>Features documentation not available.</p>"

    return render(request, 'core/help/features.html', {
        'title': 'Features',
        'content': html_content
    })


@login_required
def help_assets(request):
    """Asset management help"""
    return render(request, 'core/help/assets.html', {
        'title': 'Asset Management'
    })


@login_required
def help_vehicles(request):
    """Service vehicles help"""
    return render(request, 'core/help/vehicles.html', {
        'title': 'Service Vehicles'
    })


@login_required
def help_vault(request):
    """Password vault help"""
    return render(request, 'core/help/vault.html', {
        'title': 'Password Vault'
    })


@login_required
def help_monitoring(request):
    """Monitoring help"""
    return render(request, 'core/help/monitoring.html', {
        'title': 'Monitoring'
    })


@login_required
def help_security(request):
    """Security features help"""
    return render(request, 'core/help/security.html', {
        'title': 'Security'
    })


@login_required
def help_api(request):
    """API documentation"""
    return render(request, 'core/help/api.html', {
        'title': 'API Documentation'
    })
