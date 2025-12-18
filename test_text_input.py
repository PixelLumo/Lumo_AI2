#!/usr/bin/env python3
"""
LUMO Text Input Test
Test the LLM layer with manual text input (bypasses STT)
"""

from core.llm import ask_llm

print("=" * 60)
print("LUMO Text Input Test (LLM Layer Only)")
print("=" * 60)
print("This tests ONLY the LLM layer (core/llm.py)")
print("STT/TTS are bypassed - you type text manually")
print()
print("Commands:")
print("  Type your message (it will be sent to Ollama llama3.1)")
print("  Type 'quit' or 'exit' to stop")
print()

messages = []
WAKE_WORD = "lumo"

while True:
    try:
        # Get manual text input
        user_input = input("\nYou: ").strip()

        if not user_input:
            print("(empty input)")
            continue

        if user_input.lower() in ["quit", "exit"]:
            print("Exiting...")
            break

        # Check for wake word
        if WAKE_WORD.lower() not in user_input.lower():
            print(f"[WAKE_WORD_SKIP] No '{WAKE_WORD}' detected")
            continue

        # Remove wake word
        query = (
            user_input.replace(WAKE_WORD, "")
            .replace(WAKE_WORD.upper(), "")
            .strip()
        )

        if not query:
            print("You said my name but didn't ask me anything.")
            continue

        # Add to message history
        messages.append({"role": "user", "content": query})

        print(f"\n[LLM_CALL] Sending {len(messages)} messages to Ollama...")

        # Call LLM
        reply = ask_llm(messages)

        # Add response to history
        messages.append({"role": "assistant", "content": reply})

        # Display response
        print(f"\nLUMO: {reply}\n")
        print(f"[HISTORY] Messages in conversation: {len(messages)}")

    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Ctrl+C detected. Exiting.")
        break
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
