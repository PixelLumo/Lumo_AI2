#!/usr/bin/env python3
"""Operational improvement loop - Observe → Log → Detect → Adjust → Re-test."""

import sys
from pathlib import Path
from learning.logger import get_recent_logs, get_stats
from learning.analyzer import (
    analyze_failures,
    analyze_success_rate,
    analyze_wake_word_detection,
    find_improvement_opportunities,
)
from learning.tuner import auto_tune, get_current_thresholds
from learning.feedback import suggest_retest_scenario

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def step1_observe_behavior():
    """Step 1: Observe behavior from logs."""
    print_header("STEP 1: OBSERVE BEHAVIOR")

    logs = get_recent_logs(n=100)

    if len(logs) < 5:
        print(
            "❌ Not enough logs yet (need 5+)\n"
            "   Run LUMO for a while and try various commands first."
        )
        return None

    print(f"✅ Observing {len(logs)} recent interactions")

    # Display key metrics
    stats = get_stats()
    print("\n📊 Overall Statistics:")
    print(f"   Total Interactions: {stats['total_interactions']}")
    print(f"   Success Rate: {stats['success_rate']:.1f}%")
    print(
        f"   Successful Actions: {stats['successful_actions']} / "
        f"{stats['total_interactions']}"
    )

    return logs


def step2_log_outcomes(logs):
    """Step 2: Log outcomes are already done - summarize."""
    print_header("STEP 2: LOG OUTCOMES")

    print("✅ All interactions logged to: learning/log.jsonl")
    print("   Format: JSONL (one JSON object per line)")
    print(
        "   Fields: timestamp, wake_detected, transcript, intent, "
        "action, outcome, error"
    )
    print(f"\n   Total logged: {len(logs)} interactions")


def step3_detect_patterns(logs):
    """Step 3: Detect patterns from logs."""
    print_header("STEP 3: DETECT PATTERNS")

    # Analyze failures
    failures = analyze_failures(logs)
    print("\n❌ Failure Analysis:")
    print(f"   Total Failures: {failures['total_failures']} "
          f"({failures['failure_rate']})")
    if failures["by_type"]:
        print(f"   By Type: {failures['by_type']}")
    if failures["patterns"]:
        print("   Patterns Detected:")
        for pattern in failures["patterns"]:
            print(f"     • {pattern['intent']}: "
                  f"{pattern['failure_rate']} failure rate")
            print(f"       Error: {pattern['common_error']}")

    # Analyze success rates
    success = analyze_success_rate(logs)
    print("\n✅ Success Analysis:")
    print(f"   Overall Rate: {success['overall_success_rate']}")
    print("   By Intent:")
    for intent, stats in success["by_intent"].items():
        print(f"     • {intent}: {stats['rate']} "
              f"({stats['success']} / {stats['total']})")

    # Analyze wake word detection
    wake = analyze_wake_word_detection(logs)
    print("\n🎤 Wake Word Detection:")
    print(f"   Detection Rate: {wake['detection_rate']}")
    print(f"   Outcomes: {wake['outcomes_after_detection']}")

    # Find improvement opportunities
    improvements = find_improvement_opportunities(logs)
    print(
        f"\n💡 Improvement Opportunities: "
        f"{len(improvements['recommendations'])}"
    )
    for rec in improvements["recommendations"]:
        print(f"   [{rec['priority']}] {rec['area']}")
        print(f"   Issue: {rec['issue']}")


def step4_adjust_thresholds(logs):
    """Step 4: Adjust thresholds and rules."""
    print_header("STEP 4: ADJUST THRESHOLDS / RULES")

    print("🔍 Running auto-tuning analysis...")
    tuning = auto_tune(logs)

    print("\n📋 Current Thresholds:")
    thresholds = get_current_thresholds()
    for key, value in thresholds.items():
        if key != "last_tuned":
            print(f"   {key}: {value}")

    if tuning["suggested_adjustments"]:
        adj_count = len(tuning["suggested_adjustments"])
        print(f"\n⚠  Suggested Adjustments ({adj_count}):")
        for adjustment in tuning["suggested_adjustments"]:
            print(f"\n   Parameter: {adjustment['parameter']}")
            print(f"   Current: {adjustment['current']}")
            print(f"   Suggested: {adjustment['suggested']}")
            print(f"   Reason: {adjustment['reason']}")
            print(f"   Impact: {adjustment['impact']}")

        print(
            "\n⚡ NOTE: Adjustments are suggested but NOT automatically "
            "applied."
        )
        print(
            "   Review and test before manual activation in tuning.json"
        )
    else:
        print("\n✅ Thresholds are well-tuned - no adjustments needed")


def step5_retest(logs):
    """Step 5: Suggest re-testing scenario."""
    print_header("STEP 5: RE-TEST IN LIVE USE")

    retest = suggest_retest_scenario()

    print("\n🧪 Recommended Test Scenario:")
    print(f"   Focus Area: {retest.get('focus_area', 'General')}")
    print(
        f"   Test Goal: "
        f"{retest.get('test_scenario', 'Standard operation')}"
    )
    print(
        f"   Success Criteria: "
        f"{retest.get('success_criteria', 'Monitor performance')}"
    )

    print("\n📋 Steps to re-test:")
    print("   1. Continue normal LUMO usage")
    print("   2. Focus on the scenario above")
    print("   3. Collect 10-20 more interactions")
    print("   4. Run this script again to measure improvement")

    print("\n💾 After re-testing, run: python improvement_loop.py")


def main():
    """Run the complete improvement loop."""
    print("\n" + "🔄 " * 20)
    print("LUMO OPERATIONAL IMPROVEMENT LOOP")
    print("Observe → Log → Detect → Adjust → Re-test")
    print("🔄 " * 20)

    # Step 1: Observe
    logs = step1_observe_behavior()
    if logs is None:
        return

    # Step 2: Log
    step2_log_outcomes(logs)

    # Step 3: Detect
    step3_detect_patterns(logs)

    # Step 4: Adjust
    step4_adjust_thresholds(logs)

    # Step 5: Re-test
    step5_retest(logs)

    # Summary
    print_header("SUMMARY")
    print("✅ Analysis complete!")
    print("\n📝 Next Actions:")
    print("   1. Review the improvement opportunities above")
    print("   2. If thresholds need adjustment, update learning/tuning.json")
    print("   3. Test the adjusted system in live use")
    print("   4. Rerun this analysis after 20-50 new interactions")
    print("\n🎯 Goal: Continuous improvement through data-driven tuning")
    print()


if __name__ == "__main__":
    main()
