#!/usr/bin/env python3
"""
LUMO - Always-Listening AI Assistant
Optimized with Keyword Spotting (KWS) for wake word detection

Pipeline:
Mic Stream → VAD → [KWS] → Collect → [STT] → LLM → Response

Features:
- KWS: Detects wake word WITHOUT Whisper (90% less CPU)
- Confirmation: Asks before destructive actions
- Always-listening: Background VAD, lightweight
"""

from audio.stream import start_stream, audio_queue
from audio.vad import is_speech
from audio.buffer import wait_for_wake_word, collect_utterance
from audio.stt import transcribe
from core.llm import ask_llm
from core.confirmation import (
    is_waiting, request_confirmation, confirm, cancel, check_timeout,
)
from learning.logger import log_interaction
from ui.console import show

WAKE_WORD = "lumo"

# Destructive actions that need confirmation
DESTRUCTIVE_KEYWORDS = ["delete", "remove", "clear", "erase", "wipe"]

print("=" * 60)
print("LUMO ASSISTANT - LOCAL & OFFLINE")
print("=" * 60)
print(f"🎤 Always listening for wake word: '{WAKE_WORD}'")
print("=" * 60 + "\n")

stream = start_stream()

while True:
    try:
        # ===== CHECK CONFIRMATION TIMEOUT =====
        if is_waiting() and check_timeout():
            print("⏱ Confirmation timeout - cancelled")
            show("Confirmation timed out. Cancelled.")
            continue

        # ===== WAITING FOR CONFIRMATION RESPONSE =====
        if is_waiting():
            print("🔔 Waiting for confirmation...")
            wake_detected = wait_for_wake_word(
                audio_queue, wake_keyword=WAKE_WORD, timeout=15
            )

            if not wake_detected:
                show("Confirmation timed out.")
                log_interaction(
                    wake_detected=False,
                    transcript="",
                    outcome="cancelled",
                )
                cancel()
                continue

            print("🎤 Listening for yes/no response...")
            audio = collect_utterance(audio_queue, is_speech, timeout=2.0)

            if audio is None:
                show("Didn't hear a response. Cancelled.")
                log_interaction(
                    wake_detected=True,
                    transcript="",
                    outcome="cancelled",
                )
                cancel()
                continue

            response = transcribe(audio).lower().strip()
            print(f"[RESPONSE] {response}")

            # Check for yes/no
            if any(
                word in response
                for word in [
                    "yes", "confirm", "okay", "ok", "go ahead", "do it"
                ]
            ):
                action, params = confirm()
                print(f"✓ Confirmed: {action}")
                show(f"✓ Executing: {action}")
                log_interaction(
                    wake_detected=True,
                    transcript=response,
                    intent="confirmation",
                    action=action,
                    confirmed=True,
                    outcome="success",
                )
                # TODO: Execute action with params
                continue

            elif any(
                word in response
                for word in ["no", "cancel", "stop", "abort", "don't"]
            ):
                cancel()
                print("✗ Cancelled")
                show("Action cancelled.")
                log_interaction(
                    wake_detected=True,
                    transcript=response,
                    intent="confirmation",
                    confirmed=False,
                    outcome="cancelled",
                )
                continue

            else:
                show("Please say 'yes' or 'no'.")
                log_interaction(
                    wake_detected=True,
                    transcript=response,
                    intent="confirmation",
                    outcome="failed",
                    error="Invalid confirmation response",
                )
                continue

        # ===== PHASE 1: KWS (Lightweight Wake Word Detection) =====
        wake_detected = wait_for_wake_word(
            audio_queue, wake_keyword=WAKE_WORD, timeout=60
        )

        if not wake_detected:
            continue

        # ===== PHASE 2: Collect Speech (VAD-driven) =====
        print("🎤 Listening for command...")
        audio = collect_utterance(audio_queue, is_speech, timeout=2.0)

        if audio is None:
            print("  (No speech detected)")
            log_interaction(
                wake_detected=True,
                transcript="",
                outcome="failed",
                error="No speech detected",
            )
            continue

        # ===== PHASE 3: Transcribe (Whisper - only after wake word) =====
        print("📝 Transcribing...")
        text = transcribe(audio)
        print(f"[STT] {text}")

        command = text.lower().strip()

        if not command:
            print("  (Empty command)")
            log_interaction(
                wake_detected=True,
                transcript="",
                outcome="failed",
                error="Empty transcription",
            )
            continue

        print(f"[COMMAND] {command}")

        # ===== CHECK IF DESTRUCTIVE =====
        is_destructive = any(
            keyword in command for keyword in DESTRUCTIVE_KEYWORDS
        )

        if is_destructive:
            msg = request_confirmation(
                action="destructive_action",
                params={"command": command},
                message=f"About to execute: {command}",
            )
            log_interaction(
                wake_detected=True,
                transcript=command,
                intent="destructive_action",
                action=command,
                confirmed=None,
            )
            show(msg)
            print(msg)
            continue

        # ===== PHASE 4: LLM Response =====
        reply = ask_llm([{"role": "user", "content": command}])

        log_interaction(
            wake_detected=True,
            transcript=command,
            intent="query",
            action="llm_response",
            outcome="success",
        )

        print(f"\n🤖 LUMO: {reply}\n")
        show(reply)

        # Uncomment to enable TTS
        # speak(reply)

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Exiting...")
        break
    except Exception as e:
        print(f"[ERROR] {type(e).__name__}: {e}")
        log_interaction(
            wake_detected=False,
            transcript="",
            outcome="failed",
            error=f"{type(e).__name__}: {str(e)}",
        )
        continue
