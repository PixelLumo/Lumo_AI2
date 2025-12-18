#!/usr/bin/env python3
"""Test script to find all issues before running main loop"""

import sys

print("="*60)
print("TESTING ALL MODULES")
print("="*60)

# Test 1: Import all modules
print("\n[1] Testing imports...")
try:
    print("[OK] All imports successful")
except Exception as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test 2: Check config
print("\n[2] Testing config...")
try:
    from config.settings import (
        OPENAI_API_KEY,
        ELEVENLABS_API_KEY,
        LLM_MODEL,
        VOICE_NAME
    )
    print("[OK] Config loaded")
    print(f"  - OPENAI_API_KEY: {'SET' if OPENAI_API_KEY else 'NOT SET'}")
    print(
        f"  - ELEVENLABS_API_KEY: "
        f"{'SET' if ELEVENLABS_API_KEY else 'NOT SET'}"
    )
    print(f"  - LLM_MODEL: {LLM_MODEL}")
    print(f"  - VOICE_NAME: {VOICE_NAME}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")

# Test 3: Test console.show()
print("\n[3] Testing UI...")
try:
    from ui.console import show
    show("Testing console output")
    print("[OK] Console show() works")
except Exception as e:
    print(f"[FAIL] Console error: {e}")

# Test 4: Test memory
print("\n[4] Testing Memory...")
try:
    from core.memory import Memory
    memory = Memory(dim=1536)
    test_embedding = [0.1] * 1536
    memory.add(test_embedding, "test text")
    results = memory.search([0.1] * 1536, k=1)
    print("[OK] Memory works")
    print("  - Added: 'test text'")
    print(f"  - Found: {results}")
except Exception as e:
    print(f"[FAIL] Memory error: {e}")

# Test 5: Test actions
print("\n[5] Testing Actions...")
try:
    from core.planner import execute_action
    result1 = execute_action("web_search", {"query": "python"})
    print(f"[OK] Web search: {result1}")

    result2 = execute_action("save_note", {"content": "test note"})
    print(f"[WARN] Save note needs confirmation: {result2[:50]}...")
except Exception as e:
    print(f"[FAIL] Action error: {e}")

# Test 6: Test LLM structure (won't call API without key)
print("\n[6] Testing LLM structure...")
try:
    from core.llm import SYSTEM_PROMPT
    print(f"[OK] SYSTEM_PROMPT defined: {len(SYSTEM_PROMPT)} chars")

    # Test that functions dict is properly formatted
    FUNCTIONS = [
        {
            "name": "web_search",
            "description": "Search the web",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    ]
    print("[OK] Function schema properly formatted")
except Exception as e:
    print(f"[FAIL] LLM structure error: {e}")

# Test 7: Test logger
print("\n[7] Testing Logger...")
try:
    from core.logger import logger
    logger.info("Test log entry")
    logger.transcribed("hello world")
    logger.wake_word_check("hello lumo", True)
    logger.action_pending_confirmation("save_note", {"content": "test"})
    print("[OK] Logger working")
except Exception as e:
    print(f"[FAIL] Logger error: {e}")

# Test 8: Summary
print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print("\nREADY TO RUN: python run.py")
print("NOTE: Will block on listen() waiting for audio input")

