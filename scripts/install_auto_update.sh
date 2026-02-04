#!/bin/bash
# Install Auto-Update System for HuduGlue

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}=========================================="
echo "HuduGlue Auto-Update Installer"
echo -e "==========================================${NC}"

# Get current user
CURRENT_USER=$(whoami)
PROJECT_DIR=$(pwd)

echo "Installing auto-update system..."
echo "User: $CURRENT_USER"
echo "Project: $PROJECT_DIR"

# Create dynamic service file with actual user
cat > /tmp/huduglue-auto-update.service << EOF
[Unit]
Description=HuduGlue Auto-Update Service
After=network.target

[Service]
Type=oneshot
User=$CURRENT_USER
Group=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/scripts/auto_update.sh
StandardOutput=append:/var/log/huduglue/auto-update.log
StandardError=append:/var/log/huduglue/auto-update.log

# Environment
Environment="PATH=$PROJECT_DIR/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Security
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

# Copy service files
echo "Installing systemd service and timer..."
sudo cp /tmp/huduglue-auto-update.service /etc/systemd/system/
sudo cp deploy/huduglue-auto-update.timer /etc/systemd/system/

# Set permissions
sudo chmod 644 /etc/systemd/system/huduglue-auto-update.service
sudo chmod 644 /etc/systemd/system/huduglue-auto-update.timer

# Add sudo permissions for the update script
echo "Adding sudo permissions for auto-update..."
SUDOERS_FILE="/etc/sudoers.d/huduglue-auto-update"
cat > /tmp/huduglue-auto-update-sudoers << EOF
# Allow $CURRENT_USER to restart HuduGlue services without password
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-gunicorn.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-scheduler.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-psa-sync.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-rmm-sync.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-monitor.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl is-active huduglue-*.service
$CURRENT_USER ALL=(ALL) NOPASSWD: /bin/systemctl status huduglue-*.service
EOF

sudo cp /tmp/huduglue-auto-update-sudoers "$SUDOERS_FILE"
sudo chmod 440 "$SUDOERS_FILE"
sudo visudo -c -f "$SUDOERS_FILE"

if [ $? -ne 0 ]; then
    echo "Error: Sudoers file has syntax errors. Removing..."
    sudo rm "$SUDOERS_FILE"
    exit 1
fi

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable and start timer
echo "Enabling auto-update timer..."
sudo systemctl enable huduglue-auto-update.timer
sudo systemctl start huduglue-auto-update.timer

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Auto-Update System Installed!"
echo -e "==========================================${NC}"
echo ""
echo "Configuration:"
echo "  • Updates check: Daily at 2 AM"
echo "  • Runs on boot: After 10 minutes"
echo "  • Log file: /var/log/huduglue/auto-update.log"
echo ""
echo "Management Commands:"
echo "  • Check status:  sudo systemctl status huduglue-auto-update.timer"
echo "  • View schedule: sudo systemctl list-timers huduglue-auto-update.timer"
echo "  • Run now:       sudo systemctl start huduglue-auto-update.service"
echo "  • View logs:     tail -f /var/log/huduglue/auto-update.log"
echo "  • Disable:       sudo systemctl disable huduglue-auto-update.timer"
echo ""
echo "To test the update system now:"
echo "  sudo systemctl start huduglue-auto-update.service"
echo ""
