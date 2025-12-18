#!/usr/bin/env python3
"""Test memory functionality."""

from core.memory import Memory

def test_memory():
    mem = Memory()
    mem.add("Hello", "Hi there!")
    context = mem.get_context()
    assert len(context) > 0
    print("✓ Memory test PASSED")

if __name__ == "__main__":
    test_memory()
