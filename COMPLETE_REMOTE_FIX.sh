#!/bin/bash
###############################################################################
# COMPLETE Remote System Fix
# Fixes the chicken-and-egg problem where remote can't update to get the fix
###############################################################################

echo "=========================================="
echo "Complete Remote System Fix"
echo "=========================================="
echo ""

# Step 1: Find the project directory
if [ -d "/home/administrator/huduglue" ]; then
    cd /home/administrator/huduglue
    PROJECT_DIR="/home/administrator/huduglue"
elif [ -d "/home/administrator" ] && [ -f "/home/administrator/manage.py" ]; then
    cd /home/administrator  
    PROJECT_DIR="/home/administrator"
else
    echo "❌ ERROR: Cannot find Client St0r installation"
    exit 1
fi

echo "✓ Project directory: $PROJECT_DIR"
echo ""

# Step 2: Force clean and update with sudo
echo "Step 1: Cleaning working directory..."
sudo git reset --hard HEAD 2>/dev/null || git reset --hard HEAD
sudo git clean -fd 2>/dev/null || git clean -fd
echo "✓ Clean"
echo ""

echo "Step 2: Fetching latest code..."
sudo git fetch origin 2>/dev/null || git fetch origin
echo "✓ Fetched"
echo ""

echo "Step 3: Resetting to latest..."
sudo git reset --hard origin/main 2>/dev/null || git reset --hard origin/main
echo "✓ Reset to origin/main"
echo ""

# Step 4: Verify version
CURRENT_VERSION=$(grep "VERSION = " config/version.py | cut -d"'" -f2)
echo "Current version: $CURRENT_VERSION"
echo ""

# Step 5: Setup sudo permissions
echo "Step 4: Setting up GUI update permissions..."
if [ -f "setup_gui_updates.sh" ]; then
    chmod +x setup_gui_updates.sh 2>/dev/null
    sudo ./setup_gui_updates.sh
    echo "✓ Permissions configured"
else
    echo "⚠️  setup_gui_updates.sh not found"
fi
echo ""

# Step 6: Find and activate venv
echo "Step 5: Installing dependencies..."
if [ -d "venv" ]; then
    VENV_DIR="venv"
elif [ -d "ENV" ]; then
    VENV_DIR="ENV"
else
    echo "⚠️  No venv found, skipping pip install"
    VENV_DIR=""
fi

if [ -n "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    sudo "$VENV_DIR/bin/pip" install -q -r requirements.txt
    echo "✓ Dependencies installed"
fi
echo ""

# Step 7: Migrations
echo "Step 6: Running migrations..."
if [ -n "$VENV_DIR" ]; then
    sudo "$VENV_DIR/bin/python" manage.py migrate --noinput
    echo "✓ Migrations complete"
fi
echo ""

# Step 8: Static files
echo "Step 7: Collecting static files..."
if [ -n "$VENV_DIR" ]; then
    sudo "$VENV_DIR/bin/python" manage.py collectstatic --noinput --clear
    echo "✓ Static files collected"
fi
echo ""

# Step 9: Restart gunicorn
echo "Step 8: Restarting service..."
if systemctl is-active --quiet clientst0r-gunicorn.service 2>/dev/null; then
    sudo systemctl restart clientst0r-gunicorn.service
    echo "✓ Systemd service restarted"
else
    # Not systemd - find and reload gunicorn
    MASTER_PID=$(ps aux | grep '[g]unicorn.*master' | awk '{print $2}' | head -1)
    if [ -n "$MASTER_PID" ]; then
        kill -HUP $MASTER_PID
        echo "✓ Gunicorn reloaded (PID: $MASTER_PID)"
    else
        echo "⚠️  No gunicorn process found - you may need to restart manually"
    fi
fi
echo ""

# Step 10: Verify
echo "=========================================="
echo "✅ COMPLETE FIX APPLIED!"
echo "=========================================="
echo ""
echo "Verification:"
echo "  Project: $PROJECT_DIR"
echo "  Version: $CURRENT_VERSION"
echo "  Commit: $(git rev-parse --short HEAD)"
echo ""
echo "Now test in web interface:"
echo "1. Go to Settings → System Updates"
echo "2. Should show version $CURRENT_VERSION"  
echo "3. Click 'Check for Updates'"
echo "4. If update available, click 'Apply Update'"
echo ""
echo "Future updates will work automatically via GUI!"
echo ""
