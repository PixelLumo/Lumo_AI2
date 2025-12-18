#!/usr/bin/env python3
"""Test learning logger."""

from learning.logger import log_interaction

def test_learning():
    log_interaction("Hello", "Hi there!")
    print("✓ Learning test PASSED")

if __name__ == "__main__":
    test_learning()
