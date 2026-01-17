# HuduGlue Upgrade Notes

## ✅ v2.24.117 - AUTOMATIC Gunicorn Fix During Migration!

### What's New:
The critical Gunicorn environment fix from v2.24.113/116 now **applies automatically** when you run migrations!

### Update Process (Simplified):

```bash
cd /home/administrator
git pull origin main
python manage.py migrate
sudo systemctl restart huduglue-gunicorn.service
```

**That's it!** The `python manage.py migrate` command will automatically:
- ✅ Run the Gunicorn environment fix script
- ✅ Add `EnvironmentFile=/home/administrator/.env` to your service
- ✅ Reload systemd daemon
- ✅ Restart Gunicorn service
- ✅ Display success/error messages

### What This Fixes (Automatically):
- ❌ Demo data import failures
- ❌ Password encryption errors
- ❌ Any feature requiring environment variables from .env file

### Perfect for Multiple Servers:
This update is designed for administrators managing multiple HuduGlue servers. No need to manually run fix scripts on each server - just pull and migrate!

### Already Applied the Fix Manually?
No problem! The migration detects if the fix is already applied and won't duplicate the configuration.

---

## ⚠️ v2.24.116 - CRITICAL: Apply Environment Fix NOW!

### If You're Seeing Encryption Errors - READ THIS!

**Error you might see:**
```
Error: Demo data import failed: Encryption failed: Invalid APP_MASTER_KEY format: Incorrect padding
```

### Quick Fix (2 commands):

```bash
cd /home/administrator
./scripts/fix_gunicorn_env.sh
```

**That's it!** This fixes:
- ❌ Demo data import failures
- ❌ Password encryption errors
- ❌ Any feature requiring environment variables from .env file

### What This Version Does:
- 📢 **Emphasizes** the critical Gunicorn environment fix
- 📚 Provides clear, simple instructions
- ✅ Includes the fix script (from v2.24.113)

### Already Applied the Fix?
If you've already run `./scripts/fix_gunicorn_env.sh` after v2.24.113, you're good! This version just makes the instructions clearer for others.

---

## v2.24.115 - Bug Reporting Feature

### New Feature: Report Bugs Directly to GitHub

Users can now report bugs from HuduGlue! Click **username dropdown → Report Bug**.

**Features:**
- Submit title, description, steps to reproduce
- Upload screenshots (max 5MB)
- Auto-collect system information
- Use system GitHub PAT or your own credentials

### Upgrade:
```bash
cd /home/administrator
git pull origin main
python manage.py migrate
sudo systemctl restart huduglue-gunicorn.service
```

---

## v2.24.114 - UI Cleanup

### Changes:
- Removed duplicate "System Updates" link from settings sidebar
- System Updates now only in Admin dropdown menu

---

## v2.24.113 - Critical Fix for Demo Data Import & Password Encryption

### Issue
Demo data import was failing with error:
```
Encryption failed: Invalid APP_MASTER_KEY format: Incorrect padding
```

This occurred when:
- Importing demo data from the web UI
- Creating/editing passwords from the web UI
- Any operation requiring encryption through the web interface

**Command line operations worked fine** - only web UI operations failed.

### Root Cause
The Gunicorn systemd service was not configured to load the `.env` file, so the `APP_MASTER_KEY` environment variable was not available to the Django application when running through the web server.

### Fix Required
Add `EnvironmentFile=/home/administrator/.env` to the Gunicorn service configuration.

### Automatic Fix (Recommended)

```bash
cd /home/administrator
./scripts/fix_gunicorn_env.sh
```

This script will:
1. ✅ Check if the service file exists
2. ✅ Verify .env file exists
3. ✅ Backup the service file
4. ✅ Add EnvironmentFile configuration
5. ✅ Reload systemd and restart Gunicorn
6. ✅ Verify the service started successfully

### Manual Fix (If Needed)

1. Edit the service file:
```bash
sudo nano /etc/systemd/system/huduglue-gunicorn.service
```

2. Add this line after the `Environment="PATH=..."` line:
```ini
EnvironmentFile=/home/administrator/.env
```

3. The result should look like:
```ini
[Service]
Type=notify
User=administrator
Group=administrator
WorkingDirectory=/home/administrator
Environment="PATH=/home/administrator/venv/bin"
EnvironmentFile=/home/administrator/.env
ExecStart=/home/administrator/venv/bin/gunicorn \
    ...
```

4. Reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart huduglue-gunicorn.service
```

### Verification

After applying the fix:

1. Go to **Settings → General Settings**
2. Click **"Import Demo Data"**
3. You should see: "✓ Demo data imported successfully!"
4. Refresh the page
5. Switch to "Acme Corporation" organization
6. Verify you see:
   - 5 Documents
   - 3 Diagrams
   - 10 Assets
   - 5 Passwords
   - 5 Workflows

### Note for Fresh Installations

This fix is required for any system where the Gunicorn service was set up before v2.24.113. The fix script is idempotent and safe to run multiple times.

---

## v2.24.112 - Demo Data Import Reliability

### Changes
- Removed background threading from demo data import
- Made import synchronous for better error handling
- Automatic organization switching after import
- Improved success/error messages
- Import completes in 2-3 seconds

### Upgrade
```bash
cd /home/administrator
git pull origin main
sudo systemctl restart huduglue-gunicorn.service
```

---

## Previous Versions

See git commit history for older version notes.
