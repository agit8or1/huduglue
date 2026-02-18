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
def import_rollback(request, pk):
    """
    Rollback import job - delete all imported objects.

    This allows users to undo an import for testing/debugging purposes.
    All objects created during the import (tracked via ImportMapping) will be deleted.
    """
    job = get_object_or_404(
        ImportJob.objects.select_related('target_organization', 'started_by', 'rolled_back_by'),
        pk=pk
    )

    # Check if rollback is allowed
    if not job.can_rollback():
        if job.rolled_back_at:
            messages.error(request, f'Import already rolled back on {job.rolled_back_at} by {job.rolled_back_by}.')
        elif job.dry_run:
            messages.error(request, 'Cannot rollback a dry-run import (no data was created).')
        elif job.status != 'completed':
            messages.error(request, f'Can only rollback completed imports. Current status: {job.get_status_display()}')
        else:
            messages.error(request, 'Cannot rollback this import.')
        return redirect('imports:import_detail', pk=job.pk)

    # Get statistics for confirmation
    mapping_count = job.mappings.count()
    org_count = job.organization_mappings.count()

    if request.method == 'POST':
        try:
            # Perform rollback
            stats = job.rollback(request.user)

            # Show success message with statistics
            deleted_summary = ', '.join([f"{count} {model_name.lower()}s" for model_name, count in stats['by_type'].items()])
            messages.success(
                request,
                f"Successfully rolled back import! Deleted: {deleted_summary}. "
                f"Total: {stats['total_deleted']} objects removed."
            )

            # Show any errors
            if stats['errors']:
                for error in stats['errors']:
                    messages.warning(request, f"Warning: {error}")

            return redirect('imports:import_detail', pk=job.pk)

        except Exception as e:
            import logging
            logger = logging.getLogger('imports')
            logger.error(f"Rollback failed for import {job.id}: {str(e)}", exc_info=True)
            messages.error(request, f'Rollback failed: {str(e)}')
            return redirect('imports:import_detail', pk=job.pk)

    return render(request, 'imports/import_confirm_rollback.html', {
        'job': job,
        'mapping_count': mapping_count,
        'org_count': org_count,
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
