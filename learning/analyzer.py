"""Pattern detection and analysis from learning logs."""

from collections import Counter, defaultdict
from learning.logger import get_recent_logs


def analyze_failures(logs=None, n=100):
    """
    Identify patterns in failed interactions.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Failure patterns and statistics
    """
    if logs is None:
        logs = get_recent_logs(n)

    failures = [
        log for log in logs
        if log.get("outcome") in ("failed", "cancelled")
    ]

    if not failures:
        return {"total_failures": 0, "patterns": []}

    # Group by failure type
    failure_types = Counter(log.get("outcome") for log in failures)

    # Analyze by intent
    failures_by_intent = defaultdict(list)
    for log in failures:
        intent = log.get("intent", "unknown")
        failures_by_intent[intent].append(log)

    # Identify common error messages
    error_messages = Counter(
        log.get("error") for log in failures if log.get("error")
    )

    patterns = []
    for intent, intent_failures in failures_by_intent.items():
        rate = len(intent_failures) / len(logs) * 100
        if rate > 5:  # Only report patterns > 5%
            patterns.append({
                "intent": intent,
                "failure_count": len(intent_failures),
                "failure_rate": f"{rate:.1f}%",
                "common_error": error_messages.most_common(1)[0][0]
                if error_messages else "unknown",
            })

    return {
        "total_logs": len(logs),
        "total_failures": len(failures),
        "failure_rate": (
            f"{len(failures) / len(logs) * 100:.1f}%"
            if logs
            else "0%"
        ),
        "by_type": dict(failure_types),
        "patterns": patterns,
    }


def analyze_success_rate(logs=None, n=100):
    """
    Calculate success metrics.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Success statistics
    """
    if logs is None:
        logs = get_recent_logs(n)

    successful = [
        log for log in logs if log.get("outcome") == "success"
    ]

    by_intent = defaultdict(list)
    for log in logs:
        intent = log.get("intent", "unknown")
        by_intent[intent].append(log)

    # Calculate success rate per intent
    intent_stats = {}
    for intent, intent_logs in by_intent.items():
        successes = sum(
            1 for log in intent_logs if log.get("outcome") == "success"
        )
        intent_stats[intent] = {
            "total": len(intent_logs),
            "success": successes,
            "rate": f"{successes / len(intent_logs) * 100:.1f}%"
            if intent_logs else "0%",
        }

    return {
        "total_logs": len(logs),
        "total_successful": len(successful),
        "overall_success_rate": (
            f"{len(successful) / len(logs) * 100:.1f}%"
            if logs else "0%"
        ),
        "by_intent": intent_stats,
    }


def analyze_wake_word_detection(logs=None, n=100):
    """
    Analyze wake word detection performance.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Wake word detection metrics
    """
    if logs is None:
        logs = get_recent_logs(n)

    wake_detected = sum(
        1 for log in logs if log.get("wake_detected")
    )

    # Analyze outcomes of detected wake words
    detected_outcomes = Counter(
        log.get("outcome")
        for log in logs
        if log.get("wake_detected")
    )

    return {
        "total_logs": len(logs),
        "wake_detections": wake_detected,
        "detection_rate": (
            f"{wake_detected / len(logs) * 100:.1f}%" if logs else "0%"
        ),
        "outcomes_after_detection": dict(detected_outcomes),
    }


def analyze_confirmation_behavior(logs=None, n=100):
    """
    Analyze user confirmation patterns for destructive actions.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Confirmation statistics
    """
    if logs is None:
        logs = get_recent_logs(n)

    # Find confirmation intents
    confirmations = [
        log for log in logs if log.get("intent") == "confirmation"
    ]

    if not confirmations:
        return {
            "total_confirmations": 0,
            "confirmed": 0,
            "cancelled": 0,
            "confirmation_rate": "0%",
        }

    confirmed = sum(
        1 for log in confirmations if log.get("confirmed") is True
    )
    cancelled = sum(
        1 for log in confirmations if log.get("confirmed") is False
    )

    return {
        "total_confirmations": len(confirmations),
        "confirmed": confirmed,
        "cancelled": cancelled,
        "confirmation_rate": (
            f"{confirmed / len(confirmations) * 100:.1f}%"
        ),
    }


def find_improvement_opportunities(logs=None, n=100):
    """
    Identify specific areas for improvement.

    Args:
        logs (list, optional): Use provided logs or fetch recent
        n (int): How many recent logs to analyze

    Returns:
        dict: Recommended improvements
    """
    if logs is None:
        logs = get_recent_logs(n)

    failures = analyze_failures(logs, n)
    wake_analysis = analyze_wake_word_detection(logs, n)
    success_analysis = analyze_success_rate(logs, n)

    recommendations = []

    # Check wake word detection
    try:
        detection_rate = float(
            wake_analysis["detection_rate"].rstrip("%")
        )
        if detection_rate < 80:
            recommendations.append({
                "area": "Wake Word Detection",
                "issue": f"Only {detection_rate:.1f}% detection rate",
                "suggestion": (
                    "Increase KWS threshold sensitivity or "
                    "tune RMS pattern matching"
                ),
                "priority": "HIGH" if detection_rate < 50 else "MEDIUM",
            })
    except (ValueError, KeyError):
        pass

    # Check overall success rate
    try:
        success_rate = float(
            success_analysis["overall_success_rate"].rstrip("%")
        )
        if success_rate < 85:
            recommendations.append({
                "area": "Overall Success Rate",
                "issue": f"Only {success_rate:.1f}% success rate",
                "suggestion": (
                    "Review failure patterns by intent and adjust "
                    "corresponding thresholds"
                ),
                "priority": "HIGH" if success_rate < 70 else "MEDIUM",
            })
    except (ValueError, KeyError):
        pass

    # Check for dominant failure patterns
    for pattern in failures.get("patterns", []):
        if float(pattern["failure_rate"].rstrip("%")) > 10:
            recommendations.append({
                "area": f"{pattern['intent']} Intent",
                "issue": f"{pattern['failure_rate']} failure rate",
                "suggestion": (
                    f"Debug {pattern['intent']} intent handling. "
                    f"Common error: {pattern['common_error']}"
                ),
                "priority": "MEDIUM",
            })

    return {
        "timestamp": logs[-1].get("timestamp") if logs else None,
        "logs_analyzed": len(logs),
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
    }
