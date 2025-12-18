#!/usr/bin/env python3
"""Test actions."""

from actions.notes import save_note

def test_actions():
    result = save_note("Test note")
    print("✓ Actions test PASSED")

if __name__ == "__main__":
    test_actions()
