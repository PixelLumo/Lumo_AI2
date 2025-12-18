"""Automatic threshold adjustment based on learning patterns."""

import json
from pathlib import Path
from learning.analyzer import (
    analyze_wake_word_detection,
    find_improvement_opportunities,
)


def get_tuning_config_path():
    """Get path to tuning configuration file."""
    config_dir = Path(__file__).parent
    return config_dir / "tuning.json"


def load_tuning_config():
    """
    Load current tuning configuration.

    Returns:
        dict: Current threshold values
    """
    config_path = get_tuning_config_path()

    # Default configuration
    default_config = {
        "vad": {
            "silence_threshold": 0.01,
            "description": "RMS energy threshold for VAD",
            "min": 0.001,
            "max": 0.1,
            "tuned_at": None,
        },
        "kws": {
            "pattern_threshold": 0.3,
            "description": "RMS pattern matching threshold for wake word",
            "min": 0.1,
            "max": 0.9,
            "tuned_at": None,
        },
        "confirmation": {
            "timeout_seconds": 10,
            "description": "Time to wait for user confirmation",
            "min": 5,
            "max": 30,
            "tuned_at": None,
        },
        "staleness_check": {
            "enabled": True,
            "description": "Auto-tune after N interactions",
            "check_interval": 50,
            "tuned_at": None,
        },
    }

    if not config_path.exists():
        return default_config

    try:
        with open(config_path, "r") as f:
            loaded = json.load(f)
            # Merge with defaults to ensure all keys present
            for key in default_config:
                if key not in loaded:
                    loaded[key] = default_config[key]
            return loaded
    except Exception as e:
        print(f"⚠ Failed to load tuning config: {e}")
        return default_config


def save_tuning_config(config):
    """
    Save tuning configuration.

    Args:
        config (dict): Configuration to save
    """
    config_path = get_tuning_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"⚠ Failed to save tuning config: {e}")


def suggest_vad_adjustment(logs=None, n=100):
    """
    Suggest VAD threshold adjustment based on detection performance.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Adjustment recommendation
    """
    if logs is None:
        from learning.logger import get_recent_logs
        logs = get_recent_logs(n)

    # Analyze wake word detection success
    wake_analysis = analyze_wake_word_detection(logs, n)

    try:
        detection_rate = float(
            wake_analysis["detection_rate"].rstrip("%")
        )
    except (ValueError, KeyError):
        return None

    config = load_tuning_config()
    current_threshold = config["vad"]["silence_threshold"]

    # If detection is too low, increase sensitivity (lower threshold)
    if detection_rate < 70:
        new_threshold = max(
            current_threshold * 0.8,
            config["vad"]["min"]
        )
        return {
            "parameter": "vad.silence_threshold",
            "current": current_threshold,
            "suggested": new_threshold,
            "reason": (
                f"Detection rate {detection_rate:.1f}% is below 70%. "
                f"Lowering threshold increases sensitivity."
            ),
            "impact": "May increase false positives",
        }

    # If detection is too high, decrease sensitivity (raise threshold)
    elif detection_rate > 95:
        new_threshold = min(
            current_threshold * 1.2,
            config["vad"]["max"]
        )
        return {
            "parameter": "vad.silence_threshold",
            "current": current_threshold,
            "suggested": new_threshold,
            "reason": (
                f"Detection rate {detection_rate:.1f}% is above 95%. "
                f"Raising threshold reduces false positives."
            ),
            "impact": "May miss some speech",
        }

    return None


def suggest_kws_adjustment(logs=None, n=100):
    """
    Suggest KWS (keyword spotting) threshold adjustment.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Adjustment recommendation
    """
    if logs is None:
        from learning.logger import get_recent_logs
        logs = get_recent_logs(n)

    # Analyze failure patterns

    # Count "no wake word detected" errors
    no_wake_errors = sum(
        1 for failure in logs
        if (
            failure.get("wake_detected") is False
            and failure.get("outcome") == "failed"
        )
    )

    try:
        no_wake_rate = no_wake_errors / len(logs) * 100
    except ZeroDivisionError:
        return None

    config = load_tuning_config()
    current_threshold = config["kws"]["pattern_threshold"]

    # If wake word detection fails often, lower the threshold
    if no_wake_rate > 10:
        new_threshold = max(
            current_threshold * 0.85,
            config["kws"]["min"]
        )
        return {
            "parameter": "kws.pattern_threshold",
            "current": current_threshold,
            "suggested": new_threshold,
            "reason": (
                f"Wake word fails in {no_wake_rate:.1f}% of interactions. "
                f"Lowering threshold improves detection."
            ),
            "impact": "May increase false wake-ups",
        }

    return None


def apply_adjustment(parameter, new_value):
    """
    Apply a parameter adjustment.

    Args:
        parameter (str): Parameter path (e.g., "vad.silence_threshold")
        new_value (float): New value to apply

    Returns:
        dict: Result of adjustment
    """
    config = load_tuning_config()

    parts = parameter.split(".")
    if len(parts) == 2:
        section, key = parts
        if section in config and "tuned_at" in config[section]:
            from datetime import datetime
            config[section][key] = new_value
            config[section]["tuned_at"] = datetime.now().isoformat()
            save_tuning_config(config)

            return {
                "status": "success",
                "parameter": parameter,
                "old_value": config[section].get(key),
                "new_value": new_value,
            }

    return {
        "status": "failed",
        "reason": f"Unknown parameter: {parameter}",
    }


def auto_tune(logs=None, n=100):
    """
    Automatically suggest and apply tuning adjustments.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Results of auto-tuning
    """
    if logs is None:
        from learning.logger import get_recent_logs
        logs = get_recent_logs(n)

    recommendations = find_improvement_opportunities(logs, n)

    adjustments = []

    # Check VAD
    vad_adjust = suggest_vad_adjustment(logs, n)
    if vad_adjust:
        adjustments.append(vad_adjust)

    # Check KWS
    kws_adjust = suggest_kws_adjustment(logs, n)
    if kws_adjust:
        adjustments.append(kws_adjust)

    return {
        "logs_analyzed": len(logs),
        "suggested_adjustments": adjustments,
        "recommendations": recommendations,
        "status": "ready for manual review",
    }


def get_current_thresholds():
    """Get current threshold values for debugging."""
    config = load_tuning_config()
    return {
        "vad_silence_threshold": config["vad"]["silence_threshold"],
        "kws_pattern_threshold": config["kws"]["pattern_threshold"],
        "confirmation_timeout": config["confirmation"]["timeout_seconds"],
        "last_tuned": {
            "vad": config["vad"].get("tuned_at"),
            "kws": config["kws"].get("tuned_at"),
        },
    }
