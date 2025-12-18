#!/usr/bin/env python3
"""Utility to inspect and analyze LUMO learning logs."""

from learning.logger import get_recent_logs, get_stats, get_log_path


def show_recent_logs(n=10):
    """Display the last N log entries."""
    logs = get_recent_logs(n)

    if not logs:
        print("📭 No logs found yet.")
        return

    print(f"\n📋 Last {len(logs)} interactions:\n")
    print("=" * 100)

    for i, log in enumerate(logs, 1):
        timestamp = log.get("timestamp", "?")
        wake = "🎤" if log.get("wake_detected") else "❌"
        transcript = log.get("transcript", "")[:50]
        intent = log.get("intent", "?")
        outcome = log.get("outcome", "?")

        print(
            f"{i:2}. {timestamp} {wake} | {transcript:50} "
            f"| {intent:15} | {outcome}"
        )

    print("=" * 100)


def show_stats():
    """Display statistics from learning logs."""
    stats = get_stats()

    print("\n📊 Learning Statistics:\n")
    print(f"  Total Interactions:    {stats['total_interactions']}")
    print(f"  Wake Word Detections:  {stats['wake_word_detections']}")
    print(f"  Successful Actions:    {stats['successful_actions']}")
    print(f"  Failed Actions:        {stats['failed_actions']}")
    print(f"  Cancelled Actions:     {stats['cancelled_actions']}")
    print(f"  Success Rate:          {stats['success_rate']:.1f}%")
    print()


def show_log_file():
    """Show the raw log file path and size."""
    log_path = get_log_path()

    if log_path.exists():
        size_kb = log_path.stat().st_size / 1024
        print(f"\n📁 Log File: {log_path}")
        print(f"   Size: {size_kb:.2f} KB")
        print(f"   Lines: {sum(1 for _ in open(log_path))}")
    else:
        print(f"\n📁 Log File: {log_path} (not yet created)")
    print()


def main():
    """Main menu."""
    print("\n" + "=" * 100)
    print("LUMO LEARNING LOG ANALYZER")
    print("=" * 100)

    show_log_file()
    show_stats()
    show_recent_logs(15)

    print(
        "\n💡 Tip: Raw logs are in JSONL format "
        "(one JSON object per line)"
    )
    print(
        "   Each entry tracks: wake_detected, transcript, intent, "
        "action, outcome"
    )


if __name__ == "__main__":
    main()
