#!/bin/bash
# Check for update trigger file and run update if it exists
# This runs via cron every minute

TRIGGER_FILE="/tmp/clientst0r-update-trigger"
UPDATE_SCRIPT="/home/administrator/scripts/auto_update.sh"
LOG_FILE="/var/log/clientst0r/triggered-update.log"

# Check if trigger file exists
if [ -f "$TRIGGER_FILE" ]; then
    echo "[$(date)] Trigger file found, starting update..." >> "$LOG_FILE"

    # Remove trigger file first
    rm -f "$TRIGGER_FILE"

    # Run the update script
    cd /home/administrator
    bash "$UPDATE_SCRIPT" >> "$LOG_FILE" 2>&1

    echo "[$(date)] Update completed" >> "$LOG_FILE"
fi
