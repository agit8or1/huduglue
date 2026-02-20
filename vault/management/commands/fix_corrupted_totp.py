"""
Management command to identify and fix corrupted TOTP secrets.
"""
import base64
from django.core.management.base import BaseCommand
from vault.models import Password


class Command(BaseCommand):
    help = 'Identify and optionally clear corrupted TOTP secrets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear corrupted TOTP secrets (otherwise just report)',
        )
        parser.add_argument(
            '--org-id',
            type=int,
            help='Only check passwords in specific organization',
        )

    def handle(self, *args, **options):
        clear_corrupted = options['clear']
        org_id = options.get('org_id')

        self.stdout.write("Scanning for corrupted TOTP secrets...\n")

        # Get all passwords with TOTP secrets
        passwords = Password.objects.exclude(otp_secret='')
        if org_id:
            passwords = passwords.filter(organization_id=org_id)

        total_checked = 0
        corrupted = []
        plaintext = []
        valid = []

        for pwd in passwords:
            total_checked += 1

            # Check if plaintext
            if pwd.otp_secret.startswith('otpauth://'):
                plaintext.append(pwd)
                continue

            # Check if corrupted (too short)
            try:
                encrypted_bytes = base64.b64decode(pwd.otp_secret)
                if len(encrypted_bytes) < 28:
                    corrupted.append({
                        'id': pwd.id,
                        'title': pwd.title,
                        'org': pwd.organization.name,
                        'length': len(encrypted_bytes)
                    })
                else:
                    valid.append(pwd)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"  Warning: Password {pwd.id} ({pwd.title}) - "
                        f"Could not decode: {e}"
                    )
                )

        # Report results
        self.stdout.write(
            self.style.SUCCESS(
                f"\nResults:\n"
                f"  Total checked: {total_checked}\n"
                f"  Valid: {len(valid)}\n"
                f"  Plaintext (will auto-migrate): {len(plaintext)}\n"
                f"  Corrupted: {len(corrupted)}\n"
            )
        )

        if plaintext:
            self.stdout.write(self.style.WARNING("\nPlaintext TOTP secrets (will auto-migrate on first use):"))
            for pwd in plaintext[:10]:  # Show first 10
                self.stdout.write(f"  - {pwd.id}: {pwd.title} ({pwd.organization.name})")
            if len(plaintext) > 10:
                self.stdout.write(f"  ... and {len(plaintext) - 10} more")

        if corrupted:
            self.stdout.write(self.style.ERROR("\nCorrupted TOTP secrets:"))
            for item in corrupted:
                self.stdout.write(
                    f"  - ID {item['id']}: {item['title']} ({item['org']}) "
                    f"- {item['length']} bytes (expected 28+)"
                )

            if clear_corrupted:
                self.stdout.write(self.style.WARNING("\nClearing corrupted TOTP secrets..."))
                for item in corrupted:
                    pwd = Password.objects.get(id=item['id'])
                    pwd.otp_secret = ''
                    pwd.save(update_fields=['otp_secret'])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  Cleared: {item['id']} - {item['title']}"
                        )
                    )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"\nCleared {len(corrupted)} corrupted TOTP secrets. "
                        f"Users can now re-enter these manually."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "\nTo clear these corrupted entries, run with --clear flag:"
                    )
                )
                self.stdout.write(
                    "  python manage.py fix_corrupted_totp --clear"
                )
                self.stdout.write(
                    "\nThis will remove the corrupted data so users can re-enter TOTP secrets manually."
                )
