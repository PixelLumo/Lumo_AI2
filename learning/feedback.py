"""Real-time feedback and improvement loop integration."""

from pathlib import Path


def enable_live_feedback():
    """
    Enable real-time improvement feedback during operation.

    This should be called at startup to monitor learning progress.
    """
    feedback_file = Path(__file__).parent / "feedback.log"
    return feedback_file


def log_feedback(event, severity="INFO", details=None):
    """
    Log a feedback event for the improvement loop.

    Args:
        event (str): Type of event (e.g., "wake_word_miss", "high_error_rate")
        severity (str): INFO, WARNING, CRITICAL
        details (dict, optional): Additional context
    """
    feedback_file = enable_live_feedback()
    feedback_file.parent.mkdir(parents=True, exist_ok=True)

    import json
    from datetime import datetime

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event,
        "severity": severity,
        "details": details or {},
    }

    try:
        with open(feedback_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"⚠ Failed to log feedback: {e}")


def check_improvement_needed(logs):
    """
    Check if system needs improvement based on recent logs.

    Args:
        logs (list): Recent interaction logs

    Returns:
        dict: Improvement needs assessment
    """
    from learning.analyzer import (
        analyze_failures,
        analyze_wake_word_detection,
    )

    failures = analyze_failures(logs)
    wake = analyze_wake_word_detection(logs)

    needs = {
        "improvement_needed": False,
        "alerts": [],
    }

    # Check failure rate
    try:
        failure_rate = float(failures["failure_rate"].rstrip("%"))
        if failure_rate > 15:
            needs["improvement_needed"] = True
            needs["alerts"].append({
                "type": "high_failure_rate",
                "message": (
                    f"Failure rate {failure_rate:.1f}% is above 15% "
                    "threshold"
                ),
                "action": "Review failure patterns and adjust thresholds",
            })
            log_feedback(
                "high_failure_rate",
                "WARNING",
                {"failure_rate": failure_rate},
            )
    except (ValueError, KeyError):
        pass

    # Check wake word detection
    try:
        detection_rate = float(wake["detection_rate"].rstrip("%"))
        if detection_rate < 75:
            needs["improvement_needed"] = True
            needs["alerts"].append({
                "type": "low_wake_detection",
                "message": (
                    f"Wake word detection {detection_rate:.1f}% is below "
                    "75% threshold"
                ),
                "action": "Consider lowering KWS threshold",
            })
            log_feedback(
                "low_wake_detection",
                "WARNING",
                {"detection_rate": detection_rate},
            )
    except (ValueError, KeyError):
        pass

    return needs


def suggest_retest_scenario():
    """
    Suggest a specific scenario to retest after adjustments.

    Returns:
        dict: Retest scenario
    """
    from learning.analyzer import find_improvement_opportunities
    from learning.logger import get_recent_logs

    logs = get_recent_logs(50)
    opportunities = find_improvement_opportunities(logs)

    if not opportunities.get("recommendations"):
        return {"scenario": "No specific issues detected"}

    # Get the highest priority recommendation
    recs = opportunities["recommendations"]
    priority_recs = [r for r in recs if r.get("priority") == "HIGH"]

    if priority_recs:
        top_rec = priority_recs[0]
        return {
            "priority": "HIGH",
            "focus_area": top_rec["area"],
            "test_scenario": (
                f"Test {top_rec['area']} with various inputs "
                f"to verify adjustment effectiveness"
            ),
            "expected_outcome": (
                "Improved detection/success rate compared to baseline"
            ),
            "success_criteria": (
                "No new failures introduced, improved metric"
            ),
        }

    return {"scenario": "Standard operation - continue monitoring"}


def print_improvement_status():
    """Display current improvement status and recommendations."""
    from learning.logger import get_recent_logs
    from learning.analyzer import find_improvement_opportunities
    from learning.tuner import auto_tune

    logs = get_recent_logs(100)

    if len(logs) < 10:
        print("📊 Not enough logs yet for improvement analysis (need 10+)")
        return

    print("\n" + "=" * 70)
    print("IMPROVEMENT ANALYSIS")
    print("=" * 70)

    # Run analysis
    opportunities = find_improvement_opportunities(logs)
    tuning = auto_tune(logs)

    print(f"\n📋 Analyzed {opportunities['logs_analyzed']} interactions")

    if opportunities["recommendations"]:
        print(f"\n⚠  Found {len(opportunities['recommendations'])} "
              "improvement opportunities:\n")
        for i, rec in enumerate(opportunities["recommendations"], 1):
            print(f"  {i}. {rec['priority']} - {rec['area']}")
            print(f"     Issue: {rec['issue']}")
            print(f"     Suggestion: {rec['suggestion']}")
    else:
        print("\n✅ No critical improvements needed")

    if tuning["suggested_adjustments"]:
        print(f"\n🔧 {len(tuning['suggested_adjustments'])} parameter "
              "adjustments suggested:\n")
        for adj in tuning["suggested_adjustments"]:
            print(f"  • {adj['parameter']}")
            print(f"    {adj['current']} → {adj['suggested']}")
            print(f"    Reason: {adj['reason']}")
            print(f"    Impact: {adj['impact']}\n")

    # Suggest retest
    retest = suggest_retest_scenario()
    print(f"🧪 Next test scenario: {retest['scenario']}")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    print_improvement_status()
