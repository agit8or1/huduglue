"""
Real-time update progress tracking.
"""
import json
import time
from django.core.cache import cache


class UpdateProgress:
    """Track and report update progress."""

    def __init__(self, update_id='current'):
        self.update_id = update_id
        self.cache_key = f'update_progress_{update_id}'

    def start(self):
        """Initialize progress tracking."""
        self.set_progress({
            'status': 'running',
            'current_step': '',
            'steps_completed': [],
            'total_steps': 5,
            'logs': [],
            'started_at': time.time()
        })

    def set_progress(self, data):
        """Update progress data."""
        cache.set(self.cache_key, data, 600)  # 10 minute TTL

    def get_progress(self):
        """Get current progress."""
        return cache.get(self.cache_key) or {
            'status': 'idle',
            'current_step': '',
            'steps_completed': [],
            'total_steps': 5,
            'logs': []
        }

    def add_log(self, message, level='info'):
        """Add a log message."""
        progress = self.get_progress()
        progress['logs'].append({
            'message': message,
            'level': level,
            'timestamp': time.time()
        })
        self.set_progress(progress)

    def step_start(self, step_name):
        """Mark a step as starting."""
        progress = self.get_progress()
        progress['current_step'] = step_name
        self.set_progress(progress)
        self.add_log(f"Starting: {step_name}", 'info')

    def step_complete(self, step_name):
        """Mark a step as complete."""
        progress = self.get_progress()
        progress['steps_completed'].append(step_name)
        progress['current_step'] = ''
        self.set_progress(progress)
        self.add_log(f"Completed: {step_name}", 'success')

    def finish(self, success=True, error=None):
        """Mark update as finished."""
        progress = self.get_progress()
        progress['status'] = 'completed' if success else 'failed'
        progress['current_step'] = ''
        progress['finished_at'] = time.time()
        if error:
            progress['error'] = error
            self.add_log(f"Error: {error}", 'error')
        else:
            self.add_log("Update completed successfully!", 'success')
        self.set_progress(progress)

    def clear(self):
        """Clear progress data."""
        cache.delete(self.cache_key)
