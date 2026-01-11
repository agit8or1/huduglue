#!/bin/bash
# Quick status check script for HuduGlue
# Usage: ./check_status.sh

echo "================================"
echo "HuduGlue Status Check"
echo "================================"
echo ""

# Version
echo "📦 Version:"
cd /home/administrator
source venv/bin/activate 2>/dev/null
python manage.py shell -c "from config.version import get_version; print(f'  Current: {get_version()}')" 2>/dev/null | grep "Current:"
echo ""

# Service Status
echo "🚀 Service Status:"
systemctl is-active --quiet huduglue-gunicorn && echo "  ✅ Running" || echo "  ❌ Stopped"
echo "  Workers: $(pgrep -f gunicorn | wc -l)"
echo ""

# Git Status
echo "📝 Git Status:"
cd /home/administrator
echo "  Branch: $(git branch --show-current)"
echo "  Latest: $(git log --oneline -1)"
CHANGES=$(git status --porcelain | wc -l)
if [ "$CHANGES" -eq 0 ]; then
    echo "  Status: ✅ Clean (no uncommitted changes)"
else
    echo "  Status: ⚠️  $CHANGES uncommitted changes"
fi
echo ""

# Security Scan
echo "🔒 Security:"
pip-audit --format json 2>/dev/null | python -c "
import sys, json
try:
    data = json.load(sys.stdin)
    vulns = len(data.get('vulnerabilities', []))
    if vulns == 0:
        print('  ✅ 0 vulnerabilities')
    else:
        print(f'  ⚠️  {vulns} vulnerabilities found')
except:
    print('  ⚠️  Could not run scan')
" 2>/dev/null || echo "  ⚠️  Could not run scan"
echo ""

# Recent Errors
echo "🔍 Recent Errors (last 10 lines):"
tail -10 /var/log/itdocs/gunicorn-error.log 2>/dev/null | grep -i error | tail -5 || echo "  ✅ No recent errors"
echo ""

# Progress File
echo "📋 Session Progress:"
if [ -f .claude_session_progress.md ]; then
    echo "  ✅ Progress file exists"
    echo "  Last updated: $(stat -c %y .claude_session_progress.md | cut -d'.' -f1)"
else
    echo "  ⚠️  No progress file found"
fi
echo ""

echo "================================"
echo "To view full progress: cat /home/administrator/.claude_session_progress.md"
echo "To view rules: cat /home/administrator/.claude_rules.md"
echo "================================"
