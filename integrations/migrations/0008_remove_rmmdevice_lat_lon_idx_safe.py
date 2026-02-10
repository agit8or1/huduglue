# Generated manually to handle index removal safely
from django.db import migrations, connection


def remove_index_if_exists(apps, schema_editor):
    """
    Safely remove index if it exists.
    This handles cases where the index may not have been created.
    """
    with connection.cursor() as cursor:
        # Check if index exists before trying to drop it
        if schema_editor.connection.vendor == 'mysql':
            cursor.execute("""
                SELECT COUNT(1)
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE table_schema = DATABASE()
                AND table_name = 'integrations_rmmdevice'
                AND index_name = 'rmm_devices_lat_lon_idx'
            """)
            exists = cursor.fetchone()[0] > 0

            if exists:
                cursor.execute("DROP INDEX `rmm_devices_lat_lon_idx` ON `integrations_rmmdevice`")
        elif schema_editor.connection.vendor == 'postgresql':
            cursor.execute("""
                SELECT COUNT(1)
                FROM pg_indexes
                WHERE tablename = 'integrations_rmmdevice'
                AND indexname = 'rmm_devices_lat_lon_idx'
            """)
            exists = cursor.fetchone()[0] > 0

            if exists:
                cursor.execute("DROP INDEX IF EXISTS rmm_devices_lat_lon_idx")
        elif schema_editor.connection.vendor == 'sqlite':
            cursor.execute("""
                SELECT COUNT(1)
                FROM sqlite_master
                WHERE type = 'index'
                AND name = 'rmm_devices_lat_lon_idx'
            """)
            exists = cursor.fetchone()[0] > 0

            if exists:
                cursor.execute("DROP INDEX IF EXISTS rmm_devices_lat_lon_idx")


def reverse_remove(apps, schema_editor):
    """
    Reverse operation - recreate the index if needed.
    """
    # Note: We can't reliably recreate the index in reverse
    # If rolling back, the index should be recreated by the forward migration
    # that originally created it
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('integrations', '0007_add_site_fields_to_rmmdevice'),
    ]

    operations = [
        migrations.RunPython(remove_index_if_exists, reverse_remove),
    ]
