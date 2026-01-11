"""
Management command to run RMM sync for all active connections
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from integrations.models import RMMConnection
from integrations.sync import RMMSync
import logging

logger = logging.getLogger('integrations')


class Command(BaseCommand):
    help = 'Sync RMM data for all active connections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--connection-id',
            type=int,
            help='Sync specific connection by ID'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force sync even if recently synced'
        )
        parser.add_argument(
            '--test-only',
            action='store_true',
            help='Only test connections, do not sync'
        )

    def handle(self, *args, **options):
        connection_id = options.get('connection_id')
        force = options.get('force', False)
        test_only = options.get('test_only', False)

        if connection_id:
            # Sync specific connection
            try:
                connection = RMMConnection.objects.get(id=connection_id)
                self.sync_connection(connection, force, test_only)
            except RMMConnection.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Connection {connection_id} not found'))
                return
        else:
            # Sync all active connections
            connections = RMMConnection.objects.filter(
                is_active=True,
                sync_enabled=True
            )

            if not connections.exists():
                self.stdout.write(self.style.WARNING('No active RMM connections found'))
                return

            self.stdout.write(f'Found {connections.count()} active RMM connections')

            for connection in connections:
                self.sync_connection(connection, force, test_only)

    def sync_connection(self, connection, force=False, test_only=False):
        """Sync a single connection."""
        self.stdout.write(f'\nProcessing: {connection.name} ({connection.get_provider_type_display()})')

        # Test connection first
        if test_only:
            try:
                from integrations.providers.rmm import get_rmm_provider
                provider = get_rmm_provider(connection)
                if provider.test_connection():
                    self.stdout.write(self.style.SUCCESS('  ✓ Connection test passed'))
                else:
                    self.stdout.write(self.style.ERROR('  ✗ Connection test failed'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Connection error: {e}'))
            return

        # Check if sync is needed
        if not force and connection.last_sync_at:
            next_sync = connection.last_sync_at + timedelta(minutes=connection.sync_interval_minutes)
            if timezone.now() < next_sync:
                self.stdout.write(f'  ⏭ Skipping: next sync at {next_sync.strftime("%Y-%m-%d %H:%M")}')
                return

        try:
            syncer = RMMSync(connection)
            stats = syncer.sync_all()

            # Format stats output
            self.stdout.write(self.style.SUCCESS('  ✓ Sync completed:'))
            self.stdout.write(f'    Devices: {stats["devices"]["created"]} created, {stats["devices"]["updated"]} updated, {stats["devices"]["mapped"]} mapped to assets')
            if stats['alerts']['created'] > 0 or stats['alerts']['updated'] > 0:
                self.stdout.write(f'    Alerts: {stats["alerts"]["created"]} created, {stats["alerts"]["updated"]} updated')
            if stats['software']['created'] > 0 or stats['software']['updated'] > 0:
                self.stdout.write(f'    Software: {stats["software"]["created"]} created, {stats["software"]["updated"]} updated, {stats["software"]["deleted"]} removed')

            # Show any errors
            if stats['devices']['errors'] > 0 or stats['alerts']['errors'] > 0 or stats['software']['errors'] > 0:
                self.stdout.write(self.style.WARNING(f'    Errors: {stats["devices"]["errors"]} devices, {stats["alerts"]["errors"]} alerts, {stats["software"]["errors"]} software'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ✗ Sync failed: {e}'))
            logger.exception(f'RMM sync failed for {connection}')
