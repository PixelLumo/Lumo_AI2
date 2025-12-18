#!/usr/bin/env python3
"""Test LLM functionality."""

from core.llm import generate_response
from core.memory import Memory

def test_llm():
    mem = Memory()
    mem.add("What is the time?", "It is 3 PM")
    response = generate_response("What is your name?", mem)
    assert len(response) > 0
    print("✓ LLM test PASSED")

if __name__ == "__main__":
    test_llm()
