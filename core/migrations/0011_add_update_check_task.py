"""
Add system update check scheduled task.
"""
from django.db import migrations


def add_update_check_task(apps, schema_editor):
    """Create the update_check scheduled task."""
    ScheduledTask = apps.get_model('core', 'ScheduledTask')

    # Create update check task (runs every hour)
    ScheduledTask.objects.get_or_create(
        task_type='update_check',
        defaults={
            'description': 'Automatically check GitHub for system updates every hour',
            'enabled': True,
            'interval_minutes': 60,  # Every hour
        }
    )


def remove_update_check_task(apps, schema_editor):
    """Remove the update_check scheduled task."""
    ScheduledTask = apps.get_model('core', 'ScheduledTask')
    ScheduledTask.objects.filter(task_type='update_check').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_alter_scheduledtask_task_type'),
    ]

    operations = [
        migrations.RunPython(add_update_check_task, remove_update_check_task),
    ]
