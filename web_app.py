#!/usr/bin/env python3
"""
LUMO Web Interface
Text-based LLM testing via browser
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from core.llm import ask_llm
from core.planner import execute_action
from core.logger import logger

app = Flask(__name__)

# Session state
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

logger.info("WEB MODE started")


@app.route("/")
def index():
    return render_template("lumo_web.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    global messages, pending_confirmation, TURN_NUM

    data = request.json
    user_text = data.get("message", "").strip()

    if not user_text:
        return jsonify({"error": "Empty message"}), 400

    TURN_NUM += 1
    turn_timestamp = datetime.now().isoformat()
    turn_data = {
        "turn": TURN_NUM,
        "timestamp": turn_timestamp,
        "raw_transcript": user_text,
        "cleaned_transcript": "",
        "wake_word_detected": False,
        "final_output": "",
        "exception": None
    }

    try:
        # Handle confirmation response
        if pending_confirmation:
            if any(w in user_text.lower() for w in ["yes", "confirm", "ok"]):
                result = execute_action(
                    pending_confirmation["name"],
                    pending_confirmation["arguments"],
                    confirmed=True
                )
                turn_data["cleaned_transcript"] = user_text
                turn_data["final_output"] = result
                pending_confirmation = None
                logger.log_turn(turn_data)
                return jsonify({
                    "response": result,
                    "type": "confirmation_accepted"
                })

            elif any(w in user_text.lower() for w in ["no", "cancel", "stop"]):
                turn_data["cleaned_transcript"] = user_text
                turn_data["final_output"] = "Action cancelled"
                pending_confirmation = None
                logger.log_turn(turn_data)
                return jsonify({
                    "response": "Action cancelled.",
                    "type": "confirmation_rejected"
                })

        # Check for wake word
        if WAKE_WORD.lower() not in user_text.lower():
            turn_data["wake_word_detected"] = False
            logger.log_turn(turn_data)
            return jsonify({
                "response": f"Wake word '{WAKE_WORD}' not detected.",
                "type": "no_wake_word"
            })

        turn_data["wake_word_detected"] = True

        # Clean query
        query = (
            user_text.replace(WAKE_WORD, "")
            .replace(WAKE_WORD.upper(), "")
            .strip()
        )
        turn_data["cleaned_transcript"] = query

        if not query:
            turn_data["final_output"] = (
                "You said my name but didn't ask anything."
            )
            logger.log_turn(turn_data)
            return jsonify({
                "response": "You said my name but didn't ask me anything.",
                "type": "empty_query"
            })

        # Add to message history
        messages.append({"role": "user", "content": query})
        turn_data["llm_input_context_size"] = len(messages)

        # Call LLM
        reply = ask_llm(messages, FUNCTIONS)

        # Handle response
        if reply.get("function_call"):
            func_name = reply["function_call"]["name"]

            result = execute_action(
                func_name,
                reply["function_call"]["arguments"],
                confirmed=False
            )

            if result.startswith("NEEDS_CONFIRMATION:"):
                msg = result.replace("NEEDS_CONFIRMATION: ", "")
                turn_data["final_output"] = msg
                pending_confirmation = {
                    "name": func_name,
                    "arguments": reply["function_call"]["arguments"]
                }
                logger.log_turn(turn_data)
                return jsonify({
                    "response": msg,
                    "type": "needs_confirmation",
                    "action": func_name
                })
            else:
                turn_data["final_output"] = result
                messages.append({"role": "function", "content": result})
                logger.log_turn(turn_data)
                return jsonify({
                    "response": result,
                    "type": "function_result",
                    "action": func_name
                })

        else:
            text = reply["content"]
            turn_data["final_output"] = text
            messages.append({"role": "assistant", "content": text})
            logger.log_turn(turn_data)
            return jsonify({
                "response": text,
                "type": "text"
            })

    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        turn_data["exception"] = type(e).__name__
        logger.log_turn(turn_data)
        return jsonify({
            "error": error_msg,
            "type": "error"
        }), 500


@app.route("/api/clear", methods=["POST"])
def clear():
    global messages, pending_confirmation
    messages = []
    pending_confirmation = None
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    print("\n" + "="*60)
    print("LUMO WEB MODE")
    print("="*60)
    print("Open browser to: http://localhost:5000")
    print("Type commands like: 'lumo what time is it'")
    print("="*60 + "\n")
    app.run(debug=False, port=5000)
