#!/bin/bash
echo "=== FINAL Remote System Fix ==="
echo ""

cd /home/administrator/huduglue

echo "Step 1: Attach HEAD to main branch..."
git checkout main
echo "✓ On main branch"
echo ""

echo "Step 2: Reset to latest..."
git reset --hard origin/main
echo "✓ Reset complete"
echo ""

echo "Step 3: Verify version..."
VERSION=$(grep "VERSION = " config/version.py | cut -d"'" -f2)
echo "Version: $VERSION"
echo ""

echo "Step 4: Clear Python cache..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
echo "✓ Cache cleared"
echo ""

echo "Step 5: Restart gunicorn..."
MASTER_PID=$(ps aux | grep '[g]unicorn.*master' | awk '{print $2}' | head -1)
if [ -n "$MASTER_PID" ]; then
    kill -TERM $MASTER_PID
    sleep 3
    
    # Restart gunicorn
    cd /home/administrator/huduglue
    source venv/bin/activate
    venv/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 --timeout 120 \
        --access-logfile /var/log/itdocs/gunicorn-access.log \
        --error-logfile /var/log/itdocs/gunicorn-error.log \
        --log-level info config.wsgi:application --daemon
    
    sleep 2
    echo "✓ Gunicorn restarted"
else
    echo "⚠️ No gunicorn process found"
fi
echo ""

echo "=== SUCCESS! ==="
echo ""
echo "System should now show:"
echo "  Version: $VERSION"
echo "  Branch: main"
echo "  Status: Clean (not Modified)"
echo ""
echo "Refresh web interface and check Settings → System Updates"
echo ""
