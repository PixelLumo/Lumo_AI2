#!/usr/bin/env python3
"""Test all module imports."""

print("[TEST] Importing all modules...")
try:
    import core.llm
    import core.memory
    import core.confirmation
    import audio.stt
    import audio.tts
    import audio.vad
    import audio.kws
    import actions.notes
    import knowledge.search
    import learning.logger
    import ui.console
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)

