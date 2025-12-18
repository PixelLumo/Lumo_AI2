#!/usr/bin/env python3
"""Quick test of the learning logger."""

from learning.logger import log_interaction, get_recent_logs, get_stats

# Test logging a few interactions
print("Testing learning logger...\n")

log_interaction(
    wake_detected=True,
    transcript="lumo what time is it",
    intent="query",
    action="time_query",
    outcome="success",
)
print("✓ Logged: query - success")

log_interaction(
    wake_detected=True,
    transcript="lumo delete all my files",
    intent="destructive_action",
    action="delete",
    confirmed=None,
    outcome="pending",
)
print("✓ Logged: destructive_action - pending confirmation")

log_interaction(
    wake_detected=True,
    transcript="yes",
    intent="confirmation",
    action="delete",
    confirmed=True,
    outcome="success",
)
print("✓ Logged: confirmation - yes")

# Show stats
print("\nStats:")
stats = get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# Show recent logs
print("\nRecent logs:")
logs = get_recent_logs(5)
for i, log in enumerate(logs, 1):
    print(f"  {i}. {log['transcript'][:40]:40} → {log['outcome']}")
