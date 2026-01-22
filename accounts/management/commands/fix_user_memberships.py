"""
Management command to create default memberships for existing users without any.
Run with: python manage.py fix_user_memberships
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Membership, Role
from core.models import Organization

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default organization memberships for users without any'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Get the default organization (first active org)
        default_org = Organization.objects.filter(is_active=True).first()

        if not default_org:
            self.stdout.write(self.style.ERROR('No active organizations found!'))
            return

        self.stdout.write(f"Default organization: {default_org.name}")

        # Find users without any active memberships
        users_without_membership = []

        for user in User.objects.all():
            if user.is_superuser:
                continue  # Skip superusers

            has_membership = Membership.objects.filter(
                user=user,
                is_active=True
            ).exists()

            if not has_membership:
                users_without_membership.append(user)

        if not users_without_membership:
            self.stdout.write(self.style.SUCCESS('All users already have memberships!'))
            return

        self.stdout.write(
            f"Found {len(users_without_membership)} users without memberships"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - No changes will be made'))
            for user in users_without_membership:
                self.stdout.write(f"  Would create membership for: {user.username} ({user.email})")
            return

        # Create memberships
        created_count = 0
        for user in users_without_membership:
            Membership.objects.create(
                user=user,
                organization=default_org,
                role=Role.READONLY,
                is_active=True
            )
            created_count += 1
            self.stdout.write(f"  Created membership for: {user.username}")

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} memberships in {default_org.name}'
            )
        )
