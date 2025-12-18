"""Append-only learning log for LUMO interactions."""

import json
from datetime import datetime
from pathlib import Path


def get_log_path():
    """Get the path to the learning log JSONL file."""
    log_dir = Path(__file__).parent
    return log_dir / "log.jsonl"


def log_interaction(
    wake_detected,
    transcript,
    intent=None,
    action=None,
    confirmed=None,
    outcome=None,
    error=None
):
    """
    Append an interaction to the learning log.

    Each interaction is recorded as a single JSON line (JSONL format).

    Args:
        wake_detected (bool): Whether wake word was detected
        transcript (str): What the user said (after STT)
        intent (str, optional): Detected intent (e.g., "device_control")
        action (str, optional): Action taken (e.g., "lights_off")
        confirmed (bool, optional):
            Whether user confirmed (for destructive actions)
        outcome (str, optional):
            Result (e.g., "success", "failed", "cancelled")
        error (str, optional): Error message if applicable

    Returns:
        dict: The logged interaction record
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "wake_detected": wake_detected,
        "transcript": transcript if transcript else "",
        "intent": intent,
        "action": action,
        "confirmed": confirmed,
        "outcome": outcome,
        "error": error,
    }

    log_path = get_log_path()

    # Ensure directory exists
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Append to JSONL (one JSON object per line)
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"⚠ Failed to write learning log: {e}")

    return log_entry


def get_recent_logs(n=10):
    """
    Retrieve the last N log entries.

    Args:
        n (int): Number of recent logs to retrieve (default 10)

    Returns:
        list: List of interaction records (most recent last)
    """
    log_path = get_log_path()

    if not log_path.exists():
        return []

    logs = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    logs.append(json.loads(line))
    except Exception as e:
        print(f"⚠ Failed to read learning log: {e}")
        return []

    # Return last N entries
    return logs[-n:] if len(logs) > n else logs


def get_stats():
    """
    Get basic statistics from the learning log.

    Returns:
        dict: Statistics (total interactions, success rate, etc.)
    """
    log_path = get_log_path()

    if not log_path.exists():
        return {
            "total_interactions": 0,
            "wake_word_detections": 0,
            "successful_actions": 0,
            "failed_actions": 0,
            "success_rate": 0.0,
        }

    stats = {
        "total_interactions": 0,
        "wake_word_detections": 0,
        "successful_actions": 0,
        "failed_actions": 0,
        "cancelled_actions": 0,
    }

    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                entry = json.loads(line)
                stats["total_interactions"] += 1

                if entry.get("wake_detected"):
                    stats["wake_word_detections"] += 1

                outcome = entry.get("outcome")
                if outcome == "success":
                    stats["successful_actions"] += 1
                elif outcome == "failed":
                    stats["failed_actions"] += 1
                elif outcome == "cancelled":
                    stats["cancelled_actions"] += 1
    except Exception as e:
        print(f"⚠ Failed to compute stats: {e}")

    # Compute success rate
    total_actions = (
        stats["successful_actions"]
        + stats["failed_actions"]
        + stats["cancelled_actions"]
    )
    stats["success_rate"] = (
        (stats["successful_actions"] / total_actions * 100)
        if total_actions > 0
        else 0.0
    )

    return stats
