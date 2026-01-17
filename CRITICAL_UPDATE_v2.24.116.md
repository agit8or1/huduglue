# ⚠️ CRITICAL UPDATE: v2.24.116

## Fix Demo Data Import & Password Encryption Errors

If you're seeing errors like:
```
Error: Demo data import failed: Encryption failed: Invalid APP_MASTER_KEY format: Incorrect padding
```

This update includes the **REQUIRED FIX** for Gunicorn environment variable loading.

---

## 🔧 What This Fixes

The Gunicorn service was not loading the `.env` file, causing:
- ❌ Demo data import failures
- ❌ Password creation/editing errors from web UI
- ❌ Any encryption operations through the web interface

**Command line operations worked fine** - only web UI operations failed.

---

## 🚀 How to Apply This Update

### Step 1: Pull the Latest Code
```bash
cd /home/administrator
git pull origin main
```

### Step 2: Run the Automatic Fix Script
```bash
cd /home/administrator
./scripts/fix_gunicorn_env.sh
```

**That's it!** The script will:
- ✅ Check if the fix is already applied
- ✅ Backup your current service file
- ✅ Add `EnvironmentFile=/home/administrator/.env` to Gunicorn service
- ✅ Reload systemd daemon
- ✅ Restart Gunicorn service
- ✅ Verify the service started successfully

---

## ✅ Verification

After running the fix script, test the demo data import:

1. Go to **Settings → Demo Data Import**
2. Click **"Import Demo Data"**
3. You should see: **"✓ Demo data imported successfully!"**
4. Refresh the page and verify data appears

---

## 📋 What's Included in v2.24.116

### This Version (v2.24.116)
- ⚠️ **CRITICAL:** Emphasizes required Gunicorn environment fix
- 📚 Updated documentation and clear instructions
- ✅ Includes fix script from v2.24.113

### Previous Updates You Have

**v2.24.115** - Bug Reporting Feature
- ✅ Report bugs directly to GitHub from HuduGlue
- ✅ Screenshot support
- ✅ Auto-collected system information

**v2.24.114** - UI Cleanup
- ✅ Removed duplicate "System Updates" link from settings

**v2.24.113** - Gunicorn Environment Fix (THE FIX YOU NEED!)
- ✅ Created `fix_gunicorn_env.sh` script
- ✅ Fixes environment variable loading in Gunicorn

**v2.24.112** - Demo Data Improvements
- ✅ Removed threading from demo data import
- ✅ Automatic organization switching

---

## 🆘 Manual Fix (If Script Fails)

If the automatic script doesn't work, apply manually:

1. Edit the Gunicorn service file:
```bash
sudo nano /etc/systemd/system/huduglue-gunicorn.service
```

2. Add this line after `Environment="PATH=..."`:
```ini
EnvironmentFile=/home/administrator/.env
```

3. Reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart huduglue-gunicorn.service
```

4. Verify:
```bash
sudo systemctl status huduglue-gunicorn.service
```

---

## 💡 Why This Happened

The Gunicorn systemd service wasn't configured to load environment variables from the `.env` file. This meant `APP_MASTER_KEY` and other environment variables weren't available when running operations through the web UI.

The fix adds `EnvironmentFile=/home/administrator/.env` to the service configuration, ensuring all environment variables are properly loaded.

---

**🎯 Bottom Line: Run the fix script and your encryption errors will be gone!**

```bash
cd /home/administrator && ./scripts/fix_gunicorn_env.sh
```
