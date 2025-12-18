#!/usr/bin/env python3
"""Test all module imports."""

print("[TEST] Importing all modules...")
try:
    import core.llm
    import core.memory
    import core.confirmation  # noqa: F401
    import audio.stt
    import audio.tts
    import audio.vad
    import audio.kws  # noqa: F401
    import actions.notes  # noqa: F401
    import knowledge.search  # noqa: F401
    import learning.logger  # noqa: F401
    import ui.console  # noqa: F401
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    exit(1)
