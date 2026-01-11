"""
Views for IT Glue/Hudu import
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import ImportJob
from .forms import ImportJobForm
from .services import get_import_service
import logging

logger = logging.getLogger('imports')


def is_staff_or_superuser(user):
    """Check if user is staff or superuser."""
    return user.is_superuser or (hasattr(user, 'is_staff_user') and user.is_staff_user)


@login_required
@user_passes_test(is_staff_or_superuser)
def import_list(request):
    """List all import jobs."""
    jobs = ImportJob.objects.all().select_related('target_organization', 'started_by').order_by('-created_at')

    return render(request, 'imports/import_list.html', {
        'jobs': jobs,
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_create(request):
    """Create new import job."""
    if request.method == 'POST':
        form = ImportJobForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            job = form.save(commit=False)
            job.started_by = request.user
            job.save()

            messages.success(request, f'Import job created. Review settings and click "Start Import" to begin.')
            return redirect('imports:import_detail', pk=job.pk)
    else:
        form = ImportJobForm(user=request.user)

    return render(request, 'imports/import_form.html', {
        'form': form,
        'action': 'Create',
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_detail(request, pk):
    """View import job details."""
    job = get_object_or_404(ImportJob.objects.select_related('target_organization', 'started_by'), pk=pk)

    return render(request, 'imports/import_detail.html', {
        'job': job,
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_edit(request, pk):
    """Edit import job (only if not started)."""
    job = get_object_or_404(ImportJob, pk=pk)

    if job.status != 'pending':
        messages.error(request, 'Cannot edit import job that has already started.')
        return redirect('imports:import_detail', pk=job.pk)

    if request.method == 'POST':
        form = ImportJobForm(request.POST, request.FILES, instance=job, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Import job updated successfully.')
            return redirect('imports:import_detail', pk=job.pk)
    else:
        form = ImportJobForm(instance=job, user=request.user)

    return render(request, 'imports/import_form.html', {
        'form': form,
        'action': 'Edit',
        'job': job,
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_delete(request, pk):
    """Delete import job."""
    job = get_object_or_404(ImportJob, pk=pk)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Import job deleted.')
        return redirect('imports:import_list')

    return render(request, 'imports/import_confirm_delete.html', {
        'job': job,
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_start(request, pk):
    """Start an import job."""
    job = get_object_or_404(ImportJob, pk=pk)

    if job.status not in ['pending', 'failed']:
        messages.error(request, f'Cannot start import job with status: {job.get_status_display()}')
        return redirect('imports:import_detail', pk=job.pk)

    if request.method == 'POST':
        try:
            # Run import in the background (or could use Celery/background task)
            service = get_import_service(job)
            stats = service.run_import()

            messages.success(
                request,
                f'Import completed! '
                f'Imported: {job.items_imported}, '
                f'Skipped: {job.items_skipped}, '
                f'Failed: {job.items_failed}'
            )

        except Exception as e:
            messages.error(request, f'Import failed: {str(e)}')
            logger.exception(f'Import job {job.id} failed')

        return redirect('imports:import_detail', pk=job.pk)

    return render(request, 'imports/import_start.html', {
        'job': job,
    })


@login_required
@user_passes_test(is_staff_or_superuser)
def import_log(request, pk):
    """View import job log."""
    job = get_object_or_404(ImportJob, pk=pk)

    return render(request, 'imports/import_log.html', {
        'job': job,
    })
