"""
Quick add views for organization admins to rapidly create assets.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.middleware import get_request_organization
from core.decorators import require_admin
from .forms import QuickPCForm, QuickServerForm
from .models import Asset


@login_required
@require_admin
def quick_pc_add(request):
    """
    Quick form for creating a new PC/laptop asset.
    """
    org = get_request_organization(request)

    if request.method == 'POST':
        form = QuickPCForm(request.POST, organization=org)
        if form.is_valid():
            try:
                asset = form.save(commit=False)
                asset.organization = org
                asset.created_by = request.user
                asset.save()

                messages.success(
                    request,
                    f"PC '{asset.name}' created successfully."
                )
                return redirect('assets:asset_detail', pk=asset.pk)
            except Exception as e:
                messages.error(request, f"Error creating PC: {str(e)}")
    else:
        form = QuickPCForm(organization=org)

    return render(request, 'assets/quick_pc_form.html', {
        'form': form,
        'current_organization': org,
    })


@login_required
@require_admin
def quick_server_add(request):
    """
    Quick form for creating a new server asset.
    """
    org = get_request_organization(request)

    if request.method == 'POST':
        form = QuickServerForm(request.POST, organization=org)
        if form.is_valid():
            try:
                asset = form.save(commit=False)
                asset.organization = org
                asset.created_by = request.user
                asset.save()

                messages.success(
                    request,
                    f"Server '{asset.name}' created successfully."
                )
                return redirect('assets:asset_detail', pk=asset.pk)
            except Exception as e:
                messages.error(request, f"Error creating server: {str(e)}")
    else:
        form = QuickServerForm(organization=org)

    return render(request, 'assets/quick_server_form.html', {
        'form': form,
        'current_organization': org,
    })
