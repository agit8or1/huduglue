#!/bin/bash
# Setup Git Hooks for HuduGlue
# This script installs git hooks that automatically restart services after updates

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK_DIR="$REPO_ROOT/.git/hooks"

echo "🔧 Installing HuduGlue git hooks..."

# Create post-merge hook
cat > "$HOOK_DIR/post-merge" << 'EOF'
#!/bin/bash
# HuduGlue post-merge hook
# Automatically restart services after git pull

echo "🔄 Post-merge hook: Checking if restart is needed..."

# Check if Python files were changed
if git diff-tree -r --name-only --no-commit-id ORIG_HEAD HEAD | grep -qE '\.(py|json|txt)$'; then
    echo "📝 Python/config files changed, restarting HuduGlue services..."

    # Restart the main Gunicorn service
    if systemctl is-active --quiet huduglue-gunicorn.service; then
        echo "🔄 Restarting huduglue-gunicorn.service..."
        sudo systemctl restart huduglue-gunicorn.service

        if [ $? -eq 0 ]; then
            echo "✅ HuduGlue restarted successfully!"
        else
            echo "❌ Failed to restart HuduGlue service"
            exit 1
        fi
    else
        echo "⚠️  huduglue-gunicorn.service is not running"
    fi
else
    echo "ℹ️  No Python files changed, skipping restart"
fi

echo "✅ Post-merge hook completed"
EOF

# Make the hook executable
chmod +x "$HOOK_DIR/post-merge"

echo "✅ Git hooks installed successfully!"
echo ""
echo "The following hook was installed:"
echo "  - post-merge: Automatically restarts HuduGlue after git pull"
echo ""
echo "Note: Ensure your user has sudo permissions to restart systemd services without password:"
echo "  sudo visudo -f /etc/sudoers.d/huduglue"
echo "  # Add this line:"
echo "  administrator ALL=(ALL) NOPASSWD: /bin/systemctl restart huduglue-gunicorn.service"
