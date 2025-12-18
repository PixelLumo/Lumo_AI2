#!/usr/bin/env python3
"""
LUMO Text-Only Mode
Test the LLM without audio/TTS - just text input/output
"""

from datetime import datetime
from core.llm import ask_llm
from core.planner import execute_action
from core.logger import logger
from ui.console import show

messages = []
WAKE_WORD = "lumo"
pending_confirmation = None
TURN_NUM = 0

FUNCTIONS = [
    {
        "name": "web_search",
        "description": "Search the web",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    },
    {
        "name": "save_note",
        "description": "Save a note",
        "parameters": {
            "type": "object",
            "properties": {"content": {"type": "string"}},
            "required": ["content"]
        }
    }
]

logger.info("TEXT MODE started")
print("\n" + "="*60)
print("LUMO TEXT MODE (no audio, no TTS)")
print("="*60)
print("Type 'quit' to exit")
print("Type commands like: 'lumo what time is it'")
print("="*60 + "\n")

while True:
    try:
        TURN_NUM += 1
        turn_timestamp = datetime.now().isoformat()
        turn_data = {
            "turn": TURN_NUM,
            "timestamp": turn_timestamp,
            "raw_transcript": "",
            "cleaned_transcript": "",
            "wake_word_detected": False,
            "llm_input_context_size": 0,
            "llm_raw_response": {},
            "function_call": None,
            "final_output": "",
            "exception": None
        }

        # Get text input
        user_text = input("\nYou: ").strip()

        if not user_text:
            print("(empty input, try again)")
            continue

        if user_text.lower() == "quit":
            print("\nExiting...")
            logger.info("TEXT MODE - user exit")
            break

        turn_data["raw_transcript"] = user_text

        # Check for confirmation response
        if pending_confirmation:
            print(f"[PENDING] Waiting for: {pending_confirmation['name']}")

            if any(
                w in user_text.lower()
                for w in ["yes", "confirm", "ok", "okay"]
            ):
                print("✓ Confirmed")
                result = execute_action(
                    pending_confirmation["name"],
                    pending_confirmation["arguments"],
                    confirmed=True
                )
                turn_data["cleaned_transcript"] = user_text
                turn_data["final_output"] = result
                show(result)
                pending_confirmation = None
                logger.log_turn(turn_data)
                continue

            elif any(w in user_text.lower() for w in ["no", "cancel", "stop"]):
                print("✗ Cancelled")
                show("Action cancelled.")
                turn_data["cleaned_transcript"] = user_text
                turn_data["final_output"] = "Action cancelled"
                pending_confirmation = None
                logger.log_turn(turn_data)
                continue

        # Check for wake word
        if WAKE_WORD.lower() not in user_text.lower():
            print(f"[SKIP] No '{WAKE_WORD}' detected")
            turn_data["wake_word_detected"] = False
            logger.log_turn(turn_data)
            continue

        print(f"[WAKE] Detected '{WAKE_WORD}'")
        turn_data["wake_word_detected"] = True

        # Clean query
        query = (
            user_text.replace(WAKE_WORD, "")
            .replace(WAKE_WORD.upper(), "")
            .strip()
        )
        turn_data["cleaned_transcript"] = query

        if not query:
            show("You said my name but didn't ask me anything.")
            logger.log_turn(turn_data)
            continue

        print(f"[QUERY] {query}")
        turn_data["llm_input_context_size"] = len(messages)

        messages.append({"role": "user", "content": query})

        # Call LLM
        print("[LLM] Calling...")
        reply = ask_llm(messages, FUNCTIONS)
        turn_data["llm_raw_response"] = reply

        # Handle response
        if reply.get("function_call"):
            func_name = reply["function_call"]["name"]
            print(f"[FUNCTION] {func_name}")
            turn_data["function_call"] = {
                "name": func_name,
                "arguments": reply["function_call"]["arguments"]
            }

            result = execute_action(
                func_name,
                reply["function_call"]["arguments"],
                confirmed=False
            )

            if result.startswith("NEEDS_CONFIRMATION:"):
                msg = result.replace("NEEDS_CONFIRMATION: ", "")
                print(f"[CONFIRM] {func_name}")
                show(msg)
                pending_confirmation = {
                    "name": func_name,
                    "arguments": reply["function_call"]["arguments"]
                }
                turn_data["final_output"] = msg
            else:
                turn_data["final_output"] = result
                messages.append({"role": "function", "content": result})
                show(result)

        else:
            text = reply["content"]
            print(f"[TEXT] {len(text)} chars")
            turn_data["final_output"] = text
            messages.append({"role": "assistant", "content": text})
            show(text)

        logger.log_turn(turn_data)

    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting...")
        logger.info("TEXT MODE - interrupted")
        break
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        logger.error(type(e).__name__, str(e))
        turn_data["exception"] = type(e).__name__
        logger.log_turn(turn_data)
        continue

print("\nSession ended. Check logs:")
print("  - lumo.log (human readable)")
print("  - session_data.jsonl (structured data)")
