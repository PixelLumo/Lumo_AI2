"""
Confirmation State Machine
Handles destructive actions with user confirmation
"""

import time

class ConfirmationState:
    """Track confirmation state for destructive actions."""

    def __init__(self):
        self.waiting = False
        self.action = None
        self.params = None
        self.timestamp = None
        self.timeout = 10  # 10 seconds to confirm

    def request(self, action, params, message):
        """
        Request confirmation for an action.

        Args:
            action: Action name (e.g., "delete_note", "clear_history")
            params: Action parameters dict
            message: Confirmation message to show user

        Returns:
            str: Confirmation message
        """
        self.waiting = True
        self.action = action
        self.params = params
        self.timestamp = time.time()
        return f"🔔 {message}\n   Say 'yes' to confirm or 'no' to cancel."

    def check_timeout(self):
        """Check if confirmation has timed out."""
        if not self.waiting:
            return False

        elapsed = time.time() - self.timestamp
        if elapsed > self.timeout:
            self.clear()
            return True
        return False

    def confirm(self):
        """User confirmed the action."""
        if not self.waiting:
            return None, None

        action = self.action
        params = self.params
        self.clear()
        return action, params

    def cancel(self):
        """User cancelled the action."""
        self.clear()

    def clear(self):
        """Clear confirmation state."""
        self.waiting = False
        self.action = None
        self.params = None
        self.timestamp = None

# Singleton instance
_state = ConfirmationState()

def is_waiting():
    """Check if waiting for confirmation."""
    return _state.waiting

def request_confirmation(action, params, message):
    """Request confirmation for an action."""
    return _state.request(action, params, message)

def confirm():
    """Confirm pending action."""
    return _state.confirm()

def cancel():
    """Cancel pending action."""
    _state.cancel()

def check_timeout():
    """Check if confirmation timed out."""
    return _state.check_timeout()

def get_pending():
    """Get pending confirmation details."""
    if _state.waiting:
        return {
            "action": _state.action,
            "params": _state.params,
            "elapsed": time.time() - _state.timestamp,
            "timeout": _state.timeout
        }
    return None
