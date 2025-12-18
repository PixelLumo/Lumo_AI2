import json
from actions.web_search import web_search
from actions.notes import save_note
from core.logger import logger

# Define which actions are destructive and need confirmation
DESTRUCTIVE_ACTIONS = {
    "save_note": True,  # Writes to disk
    "web_search": False  # Read-only
}

def execute_action(name, arguments, confirmed=False):
    """
    Execute an action based on name and arguments.
    Destructive actions require confirmation.

    Args:
        name: Name of the action (web_search, save_note)
        arguments: JSON string or dict of arguments
        confirmed: Whether destructive action was confirmed

    Returns:
        str: Result of the action, or request for confirmation
    """
    # Parse arguments if they're a JSON string
    if isinstance(arguments, str):
        try:
            args = json.loads(arguments)
        except (json.JSONDecodeError, TypeError):
            args = {}
    else:
        args = arguments

    # Check if action needs confirmation
    if DESTRUCTIVE_ACTIONS.get(name) and not confirmed:
        if name == "save_note":
            content = args.get("content", "")
            logger.action_pending_confirmation(name, str(args))
            return (
                "NEEDS_CONFIRMATION: Save note with content: "
                f"'{content}'. Say 'yes' to confirm."
            )

    # Execute the action
    try:
        if name == "web_search":
            result = web_search(args.get("query", ""))
            logger.action_executed(name, str(args), result)
            return result
        if name == "save_note":
            result = save_note(args.get("content", ""))
            logger.action_executed(name, str(args), result)
            logger.action_confirmed(name, confirmed)
            return result

        result = "Action not implemented."
        logger.error("ACTION", f"Unknown action: {name}")
        return result

    except Exception as e:
        logger.error("ACTION", f"{name}: {str(e)}")
        raise
