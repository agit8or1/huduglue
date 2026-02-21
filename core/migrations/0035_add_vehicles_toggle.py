# Generated migration for vehicles feature toggle

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_add_system_package_scan'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemsetting',
            name='vehicles_enabled',
            field=models.BooleanField(default=True, help_text='Enable service vehicle fleet management features'),
        ),
    ]
