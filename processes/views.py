"""
Process views - CRUD operations for processes
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.forms import inlineformset_factory
from django.db.models import Q, Count

from core.middleware import get_request_organization
from .models import Process, ProcessStage, ProcessExecution, ProcessStageCompletion
from .forms import ProcessForm, ProcessStageFormSet, ProcessExecutionForm


def is_superuser(user):
    return user.is_superuser


@login_required
def process_list(request):
    """List all processes (org + global)"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    # Get org processes + global processes
    processes = Process.objects.filter(
        Q(organization=org) | Q(is_global=True),
        is_published=True,
        is_archived=False
    ).select_related('created_by').prefetch_related('tags')

    # Filter by category
    category = request.GET.get('category')
    if category:
        processes = processes.filter(category=category)

    # Search
    q = request.GET.get('q')
    if q:
        processes = processes.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    return render(request, 'processes/process_list.html', {
        'processes': processes,
        'current_organization': org,
        'categories': Process.CATEGORY_CHOICES,
        'selected_category': category,
    })


@login_required
def process_detail(request, slug):
    """View process details with all stages"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    process = get_object_or_404(
        Process.objects.filter(Q(organization=org) | Q(is_global=True)),
        slug=slug
    )

    # Get all stages with linked entities
    stages = process.stages.all().select_related(
        'linked_document',
        'linked_password',
        'linked_asset',
        'linked_secure_note'
    )

    # Get user's active executions for this process
    my_executions = ProcessExecution.objects.filter(
        process=process,
        organization=org,
        assigned_to=request.user,
        status__in=['not_started', 'in_progress']
    )

    return render(request, 'processes/process_detail.html', {
        'process': process,
        'stages': stages,
        'current_organization': org,
        'my_executions': my_executions,
    })


@login_required
def process_create(request):
    """Create new process"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    if request.method == 'POST':
        form = ProcessForm(request.POST, organization=org)
        formset = ProcessStageFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            process = form.save(commit=False)
            process.organization = org
            process.created_by = request.user
            process.last_modified_by = request.user
            process.save()
            form.save_m2m()

            # Save stages
            formset.instance = process
            formset.save()

            messages.success(request, f"Process '{process.title}' created successfully.")
            return redirect('processes:process_detail', slug=process.slug)
    else:
        form = ProcessForm(organization=org)
        formset = ProcessStageFormSet()

    return render(request, 'processes/process_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Create',
        'current_organization': org,
    })


@login_required
def process_edit(request, slug):
    """Edit existing process"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    process = get_object_or_404(Process, slug=slug, organization=org)

    if request.method == 'POST':
        form = ProcessForm(request.POST, instance=process, organization=org)
        formset = ProcessStageFormSet(request.POST, instance=process)

        if form.is_valid() and formset.is_valid():
            process = form.save(commit=False)
            process.last_modified_by = request.user
            process.save()
            form.save_m2m()

            formset.save()

            messages.success(request, f"Process '{process.title}' updated successfully.")
            return redirect('processes:process_detail', slug=process.slug)
    else:
        form = ProcessForm(instance=process, organization=org)
        formset = ProcessStageFormSet(instance=process)

    return render(request, 'processes/process_form.html', {
        'form': form,
        'formset': formset,
        'process': process,
        'action': 'Edit',
        'current_organization': org,
    })


@login_required
def process_delete(request, slug):
    """Delete process"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    process = get_object_or_404(Process, slug=slug, organization=org)

    if request.method == 'POST':
        title = process.title
        process.delete()
        messages.success(request, f"Process '{title}' deleted successfully.")
        return redirect('processes:process_list')

    # Check if process has active executions
    active_executions = ProcessExecution.objects.filter(
        process=process,
        status__in=['not_started', 'in_progress']
    ).count()

    return render(request, 'processes/process_confirm_delete.html', {
        'process': process,
        'active_executions': active_executions,
        'current_organization': org,
    })


# Global Processes (Superuser only)
@login_required
@user_passes_test(is_superuser)
def global_process_list(request):
    """List global processes (superuser only)"""
    processes = Process.objects.filter(is_global=True).select_related('created_by')
    
    return render(request, 'processes/global_process_list.html', {
        'processes': processes,
        'categories': Process.CATEGORY_CHOICES,
    })


@login_required
@user_passes_test(is_superuser)
def global_process_create(request):
    """Create global process (superuser only)"""
    if request.method == 'POST':
        form = ProcessForm(request.POST, is_global=True)
        formset = ProcessStageFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            process = form.save(commit=False)
            process.is_global = True
            process.created_by = request.user
            process.last_modified_by = request.user
            # Use a default org (first one) for global processes
            from core.models import Organization
            process.organization = Organization.objects.first()
            process.save()
            form.save_m2m()

            formset.instance = process
            formset.save()

            messages.success(request, f"Global process '{process.title}' created successfully.")
            return redirect('processes:global_process_list')
    else:
        form = ProcessForm(is_global=True)
        formset = ProcessStageFormSet()

    return render(request, 'processes/global_process_form.html', {
        'form': form,
        'formset': formset,
        'action': 'Create',
    })


# Process Execution
@login_required
def execution_create(request, slug):
    """Create a process execution"""
    org = get_request_organization(request)
    if not org:
        messages.error(request, 'Organization context required.')
        return redirect('accounts:organization_list')

    process = get_object_or_404(
        Process.objects.filter(Q(organization=org) | Q(is_global=True)),
        slug=slug
    )

    if request.method == 'POST':
        form = ProcessExecutionForm(request.POST, organization=org)
        if form.is_valid():
            execution = form.save(commit=False)
            execution.process = process
            execution.organization = org
            execution.started_by = request.user
            execution.started_at = timezone.now()
            execution.status = 'in_progress'
            execution.save()

            # Create stage completion records
            for stage in process.stages.all():
                ProcessStageCompletion.objects.create(
                    execution=execution,
                    stage=stage,
                    is_completed=False
                )

            messages.success(request, f"Started execution of '{process.title}'.")
            return redirect('processes:execution_detail', pk=execution.pk)
    else:
        form = ProcessExecutionForm(
            organization=org,
            initial={'assigned_to': request.user}
        )

    return render(request, 'processes/execution_form.html', {
        'form': form,
        'process': process,
        'current_organization': org,
    })


@login_required
def execution_detail(request, pk):
    """View execution with stage completion tracking"""
    org = get_request_organization(request)
    execution = get_object_or_404(ProcessExecution, pk=pk, organization=org)

    # Get stage completions
    completions = execution.stage_completions.all().select_related('stage')

    return render(request, 'processes/execution_detail.html', {
        'execution': execution,
        'completions': completions,
        'current_organization': org,
    })


@login_required
def stage_complete(request, pk):
    """Mark a stage as complete (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    completion = get_object_or_404(ProcessStageCompletion, pk=pk)
    
    # Check permissions
    org = get_request_organization(request)
    if completion.execution.organization != org:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    completion.is_completed = True
    completion.completed_by = request.user
    completion.completed_at = timezone.now()
    completion.save()

    # Check if all stages complete -> mark execution complete
    if completion.execution.stage_completions.filter(is_completed=False).count() == 0:
        completion.execution.status = 'completed'
        completion.execution.completed_at = timezone.now()
        completion.execution.save()

    return JsonResponse({
        'success': True,
        'completion_percentage': completion.execution.completion_percentage
    })


@login_required
def stage_reorder(request, slug):
    """Reorder stages via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    org = get_request_organization(request)
    process = get_object_or_404(Process, slug=slug, organization=org)

    import json
    data = json.loads(request.body)
    stage_orders = data.get('stages', [])

    for item in stage_orders:
        stage_id = item['id']
        new_order = item['order']
        ProcessStage.objects.filter(id=stage_id, process=process).update(order=new_order)

    return JsonResponse({'success': True})
