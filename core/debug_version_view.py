from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def debug_version(request):
    """Show exactly what the running code sees."""
    import sys
    import importlib
    
    html = "<html><body style='font-family: monospace; padding: 20px;'>"
    html += "<h1>Version Debug</h1><pre>"
    
    # Force reload the version module
    if 'config.version' in sys.modules:
        importlib.reload(sys.modules['config.version'])
    
    from config.version import VERSION, get_version
    
    html += f"VERSION constant: {VERSION}\n"
    html += f"get_version(): {get_version()}\n"
    
    # Check file on disk
    with open('/home/administrator/huduglue/config/version.py', 'r') as f:
        for line in f:
            if 'VERSION =' in line:
                html += f"File on disk: {line.strip()}\n"
                break
    
    html += f"\nPython module cache: {sys.modules.get('config.version')}\n"
    html += "</pre></body></html>"
    
    return HttpResponse(html)
