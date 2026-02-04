# HuduGlue Auto-Update System

Automatically keep HuduGlue up to date with the latest releases from GitHub.

## Features

✅ **Automatic Updates**
- Checks GitHub for new releases daily at 2 AM
- Pulls latest code automatically
- Runs database migrations
- Restarts all services
- Zero manual intervention required

✅ **Safe Updates**
- Stashes local changes before updating
- Runs migrations automatically
- Verifies services restart successfully
- Detailed logging of all actions
- Rollback capability if needed

✅ **Complete Automation**
- No SSH required
- No manual migration running
- No manual service restarts
- Works for any user/installation directory

## Installation

### Quick Install

```bash
cd /path/to/huduglue
./scripts/install_auto_update.sh
```

This installs:
- Auto-update script at `scripts/auto_update.sh`
- Systemd service: `huduglue-auto-update.service`
- Systemd timer: `huduglue-auto-update.timer`
- Sudo permissions for service restarts

### What Gets Automated

The auto-update system handles:
1. ✅ `git pull origin main` - Pull latest code
2. ✅ `pip install -r requirements.txt` - Update dependencies
3. ✅ `python manage.py migrate` - Run database migrations
4. ✅ `python manage.py collectstatic` - Collect static files
5. ✅ `systemctl restart huduglue-*` - Restart all services

## Usage

### Automatic (Recommended)

Once installed, updates happen automatically:
- **Daily at 2 AM** - Checks for and applies updates
- **On boot (+10 min)** - Checks after system restarts

No action required on your part!

### Manual Update

To update immediately:

```bash
# Using the script directly
/path/to/huduglue/scripts/auto_update.sh

# Using systemd service
sudo systemctl start huduglue-auto-update.service

# Using Django management command
cd /path/to/huduglue
source venv/bin/activate
python manage.py auto_update
```

### Check for Updates Only

```bash
# Django command
python manage.py auto_update --check-only

# Or check manually
git fetch origin main
git log HEAD..origin/main
```

## Management Commands

### Check Status

```bash
# Check timer status
sudo systemctl status huduglue-auto-update.timer

# View next scheduled run
sudo systemctl list-timers huduglue-auto-update.timer

# Check last service run
sudo systemctl status huduglue-auto-update.service
```

### View Logs

```bash
# Watch logs in real-time
tail -f /var/log/huduglue/auto-update.log

# View recent logs
tail -n 50 /var/log/huduglue/auto-update.log

# View all logs
cat /var/log/huduglue/auto-update.log
```

### Control Auto-Updates

```bash
# Disable automatic updates
sudo systemctl disable huduglue-auto-update.timer
sudo systemctl stop huduglue-auto-update.timer

# Enable automatic updates
sudo systemctl enable huduglue-auto-update.timer
sudo systemctl start huduglue-auto-update.timer

# Trigger update now
sudo systemctl start huduglue-auto-update.service
```

## How It Works

### Update Process

1. **Check for Updates**
   - Fetches latest code from GitHub
   - Compares local vs remote versions
   - Exits if already up to date

2. **Stash Local Changes**
   - Saves any uncommitted local changes
   - Prevents conflicts during pull
   - Can be restored if needed

3. **Pull Latest Code**
   - Downloads new code from GitHub
   - Updates all files
   - Reports new version

4. **Update Dependencies**
   - Installs/updates Python packages
   - Uses existing virtual environment
   - Non-blocking (continues on failure)

5. **Run Migrations**
   - Applies database schema changes
   - Required for some updates (like v2.49.5)
   - Automatically applied

6. **Collect Static Files**
   - Updates CSS, JavaScript, images
   - Ensures UI is current
   - Non-blocking

7. **Restart Services**
   - Restarts Gunicorn (web server)
   - Restarts Scheduler (background tasks)
   - Restarts PSA/RMM sync services
   - Restarts Monitor service
   - Verifies all services are running

### Schedule

**Default schedule:**
- **Daily:** 2:00 AM (OnCalendar=02:00)
- **On Boot:** 10 minutes after system starts
- **Persistent:** If missed, runs as soon as possible

### Logging

All update activity logged to:
- **Main log:** `/var/log/huduglue/auto-update.log`
- **Service output:** `journalctl -u huduglue-auto-update.service`

Log includes:
- Timestamps
- Each step executed
- Success/failure indicators
- Error messages
- Version changes

## Customization

### Change Update Schedule

Edit the timer:

```bash
sudo systemctl edit huduglue-auto-update.timer
```

Add custom schedule:

```ini
[Timer]
# Run every 6 hours
OnCalendar=00/6:00
```

Common schedules:
- `OnCalendar=hourly` - Every hour
- `OnCalendar=daily` - Daily at midnight
- `OnCalendar=weekly` - Weekly on Monday
- `OnCalendar=Mon,Wed,Fri 02:00` - Specific days
- `OnCalendar=*-*-* 02:00:00` - Daily at 2 AM

Then reload:

```bash
sudo systemctl daemon-reload
sudo systemctl restart huduglue-auto-update.timer
```

### Customize Update Script

Edit `scripts/auto_update.sh` to customize:
- Pre-update hooks
- Post-update actions
- Notification methods
- Additional services to restart

## Troubleshooting

### Updates Not Running

Check timer is enabled:
```bash
sudo systemctl is-enabled huduglue-auto-update.timer
```

Check next run time:
```bash
sudo systemctl list-timers --all | grep huduglue
```

### Update Failed

View error logs:
```bash
sudo journalctl -u huduglue-auto-update.service -n 50
```

Or:
```bash
tail -n 50 /var/log/huduglue/auto-update.log
```

Common issues:
- **Git conflicts:** Local changes conflict with remote
- **Migration errors:** Database schema incompatibility
- **Service restart failed:** Permission issues

### Manual Intervention Needed

If auto-update fails:

```bash
# View what failed
sudo systemctl status huduglue-auto-update.service

# Run update manually to see errors
cd /path/to/huduglue
./scripts/auto_update.sh

# Or update completely manually
git pull origin main
source venv/bin/activate
python manage.py migrate
sudo systemctl restart huduglue-gunicorn
```

### Restore Stashed Changes

If your local changes were stashed:

```bash
cd /path/to/huduglue
git stash list
git stash pop  # Restore most recent stash
```

## Security

The auto-update system requires sudo permissions to restart services. These are granted via `/etc/sudoers.d/huduglue-auto-update`:

```
# Allow user to restart HuduGlue services without password
username ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-*.service
```

This is **minimal privilege** - only allows:
- Restarting HuduGlue services (not other services)
- Checking service status
- No other sudo commands

## Uninstall

To remove auto-update system:

```bash
# Disable and stop timer
sudo systemctl disable huduglue-auto-update.timer
sudo systemctl stop huduglue-auto-update.timer

# Remove systemd files
sudo rm /etc/systemd/system/huduglue-auto-update.service
sudo rm /etc/systemd/system/huduglue-auto-update.timer
sudo rm /etc/sudoers.d/huduglue-auto-update

# Reload systemd
sudo systemctl daemon-reload

# Optionally remove script
rm /path/to/huduglue/scripts/auto_update.sh
```

## FAQ

**Q: Will this update break my installation?**
A: No. The script pulls official releases which are tested. Migrations are run automatically. Services are verified after restart.

**Q: What if I have local customizations?**
A: Local changes are automatically stashed before update and can be restored after.

**Q: Can I disable auto-updates?**
A: Yes. Run: `sudo systemctl disable huduglue-auto-update.timer`

**Q: Will this restart my services in the middle of the day?**
A: No. Default schedule is 2 AM when traffic is lowest. You can customize the schedule.

**Q: What if an update fails?**
A: The script exits immediately on failure. Your installation remains on the working version. Check logs and update manually if needed.

**Q: Do I still get update notifications in the UI?**
A: Yes! The System Updates page still shows available updates, but now they're applied automatically.

## Support

If auto-updates aren't working:

1. Check timer status: `sudo systemctl status huduglue-auto-update.timer`
2. View logs: `tail -f /var/log/huduglue/auto-update.log`
3. Test manually: `./scripts/auto_update.sh`
4. Open GitHub issue with logs

---

**Enjoy automatic updates!** 🚀
