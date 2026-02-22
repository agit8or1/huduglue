#!/bin/bash
###############################################################################
# ONE-COMMAND FIX for GUI Updates
# Run this on remote systems to enable GUI update button
###############################################################################

echo "=========================================="
echo "Enabling GUI Updates - Client St0r"
echo "=========================================="
echo ""

# Auto-detect project directory
if [ -d "/home/administrator/huduglue" ]; then
    cd /home/administrator/huduglue
    echo "✓ Found project in: /home/administrator/huduglue"
elif [ -d "/home/administrator" ] && [ -f "/home/administrator/manage.py" ]; then
    cd /home/administrator
    echo "✓ Found project in: /home/administrator"
else
    echo "❌ ERROR: Cannot find Client St0r installation"
    exit 1
fi

echo ""
echo "Step 1: Pulling latest code..."
git pull origin main || { echo "❌ Git pull failed"; exit 1; }
echo "✓ Code updated"

echo ""
echo "Step 2: Setting up GUI update permissions..."
if [ -f "setup_gui_updates.sh" ]; then
    chmod +x setup_gui_updates.sh
    sudo ./setup_gui_updates.sh || { echo "❌ Setup failed"; exit 1; }
else
    echo "❌ ERROR: setup_gui_updates.sh not found"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ SUCCESS! GUI Updates Enabled!"
echo "=========================================="
echo ""
echo "Now go to the web interface:"
echo "  Settings → System Updates"
echo "  Click 'Apply Update' button"
echo ""
echo "All future updates = ONE CLICK! 🎉"
echo ""
