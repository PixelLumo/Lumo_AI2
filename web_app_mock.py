#!/usr/bin/env python3
"""
LUMO Mock LLM Mode
Simulates responses without calling OpenAI API
Features: Notes, Weather, Calculator, Time, Search, Memory
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from core.planner import execute_action
from core.logger import logger
import core.llm

# ========== PERSISTENT STORAGE ==========
NOTES_FILE = "data/notes.json"
Path("data").mkdir(exist_ok=True)

def load_notes():
    """Load notes from file"""
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []

def save_notes_to_file(notes):
    """Save notes to file"""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)

# ========== MOCK WEATHER DATA ==========
WEATHER_DATA = {
    "new york": {"temp": 45, "condition": "Cloudy", "humidity": 65},
    "san francisco": {"temp": 58, "condition": "Sunny", "humidity": 70},
    "london": {"temp": 42, "condition": "Rainy", "humidity": 80},
    "tokyo": {"temp": 35, "condition": "Clear", "humidity": 45},
    "sydney": {"temp": 72, "condition": "Sunny", "humidity": 60},
}

# ========== CALCULATOR HELPER ==========
def evaluate_math(expr):
    """Safely evaluate simple math expressions"""
    try:
        # Only allow numbers, operators, spaces, and parentheses
        allowed = set("0123456789+-*/(). ")
        if all(c in allowed for c in expr):
            result = eval(expr)
            return f"{expr} = {result}"
    except (ValueError, TypeError, SyntaxError, ZeroDivisionError):
        return "Invalid calculation"
    return "Invalid calculation"

# ========== MOCK LLM ==========
def mock_ask_llm(messages, functions=None):
    """Simulate LLM responses with enhanced features"""

    # Get the last user message
    user_msg = ""
    for msg in reversed(messages):
        if msg["role"] == "user":
            user_msg = msg["content"].lower()
            break

    # ===== WEB SEARCH =====
    if "search" in user_msg:
        query = user_msg.replace("search", "").replace("for", "").strip()
        return {
            "content": "",
            "function_call": {
                "name": "web_search",
                "arguments": '{"query": "' + query + '"}'
            }
        }

    # ===== NOTES =====
    elif "save" in user_msg or "note" in user_msg:
        content = user_msg.replace("save", "").replace("my", "").strip()
        return {
            "content": "",
            "function_call": {
                "name": "save_note",
                "arguments": '{"content": "' + content + '"}'
            }
        }

    elif "list" in user_msg and "note" in user_msg:
        notes = load_notes()
        if not notes:
            return {
                "content": "You have no saved notes yet.",
                "function_call": None
            }
        note_list = "\n".join(
            [f"\u2022 {n.get('content', 'Untitled')}" for n in notes]
        )
        return {"content": f"Your notes:\n{note_list}", "function_call": None}

    elif "delete" in user_msg and "note" in user_msg:
        notes = load_notes()
        if not notes:
            return {"content": "No notes to delete.", "function_call": None}
        # Delete the oldest note
        notes.pop(0)
        save_notes_to_file(notes)
        return {"content": "Oldest note deleted.", "function_call": None}

    # ===== WEATHER =====
    elif "weather" in user_msg or "temperature" in user_msg:
        location = "new york"  # default
        for city in WEATHER_DATA.keys():
            if city in user_msg:
                location = city
                break

        weather = WEATHER_DATA[location]
        return {
            "content": (
                f"Weather in {location.title()}: {weather['temp']}°F, "
                f"{weather['condition']}, {weather['humidity']}% humidity"
            ),
            "function_call": None
        }

    # ===== CALCULATOR =====
    elif (
        any(op in user_msg for op in ["+", "-", "*", "/"])
        or "calculate" in user_msg
        or "math" in user_msg
    ):
        # Extract math expression
        expr = user_msg.replace("calculate", "").replace("math", "").strip()
        # Simple extraction: try to find operators and numbers
        numbers = re.findall(r'\d+\.?\d*', expr)
        if numbers:
            expr = (
                user_msg.replace("calculate", "")
                .replace("math", "")
                .replace("lumo", "")
                .strip()
            )
            result = evaluate_math(expr)
            return {"content": result, "function_call": None}

    # ===== TIME =====
    elif "time" in user_msg:
        now = datetime.now().strftime('%I:%M %p')
        return {
            "content": f"The current time is {now}",
            "function_call": None
        }

    # ===== GREETING =====
    elif "hello" in user_msg or "hi" in user_msg or "hey" in user_msg:
        notes_count = len(load_notes())
        return {
            "content": (
                f"Hello! I'm LUMO. You have {notes_count} saved notes. "
                "How can I help?"
            ),
            "function_call": None
        }

    # ===== ABOUT =====
    elif "name" in user_msg or "yourself" in user_msg or "about" in user_msg:
        return {
            "content": (
                "I'm LUMO, your AI assistant. I can:\n"
                "\u2022 Search the web\n"
                "\u2022 Save and list notes\n"
                "\u2022 Check the weather\n"
                "\u2022 Do basic math\n"
                "\u2022 Tell you the time\n\n"
                "What can I help with?"
            ),
            "function_call": None
        }

    # ===== HELP =====
    elif "help" in user_msg or "commands" in user_msg:
        return {
            "content": (
                "Available commands:\n"
                "\u2022 'lumo what time is it' - Get current time\n"
                "\u2022 'lumo search for X' - Search the web\n"
                "\u2022 'lumo save X' - Save a note\n"
                "\u2022 'lumo list notes' - Show all notes\n"
                "\u2022 'lumo delete note' - Delete oldest note\n"
                "\u2022 'lumo weather in X' - Get weather\n"
                "\u2022 'lumo calculate X' - Do math"
            ),
            "function_call": None
        }

    # ===== DEFAULT =====
    else:
        return {
            "content": (
                f"I heard: '{user_msg}'. Try 'lumo help' "
                "for available commands."
            ),
            "function_call": None
        }

# Monkey-patch the real ask_llm with mock
core.llm.ask_llm = mock_ask_llm

app = Flask(__name__)

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

logger.info("MOCK MODE started")

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

    try:
        # Handle confirmation
        if pending_confirmation:
            if any(w in user_text.lower() for w in ["yes", "confirm", "ok"]):
                result = execute_action(
                    pending_confirmation["name"],
                    pending_confirmation["arguments"],
                    confirmed=True
                )
                pending_confirmation = None
                return jsonify({
                    "response": result,
                    "type": "confirmation_accepted"
                })

            elif any(w in user_text.lower() for w in ["no", "cancel", "stop"]):
                pending_confirmation = None
                return jsonify({
                    "response": "Action cancelled.",
                    "type": "confirmation_rejected"
                })

        # Check wake word
        if WAKE_WORD.lower() not in user_text.lower():
            return jsonify({
                "response": f"Wake word '{WAKE_WORD}' not detected.",
                "type": "no_wake_word"
            })

        # Clean query
        query = (
            user_text.replace(WAKE_WORD, "")
            .replace(WAKE_WORD.upper(), "")
            .strip()
        )

        if not query:
            return jsonify({
                "response": "You said my name but didn't ask me anything.",
                "type": "empty_query"
            })

        # Add to history
        messages.append({"role": "user", "content": query})

        # Call MOCK LLM
        reply = mock_ask_llm(messages, FUNCTIONS)

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
                pending_confirmation = {
                    "name": func_name,
                    "arguments": reply["function_call"]["arguments"]
                }
                return jsonify({
                    "response": msg,
                    "type": "needs_confirmation",
                    "action": func_name
                })
            else:
                messages.append({"role": "function", "content": result})
                return jsonify({
                    "response": result,
                    "type": "function_result",
                    "action": func_name
                })

        else:
            text = reply["content"]
            messages.append({"role": "assistant", "content": text})
            return jsonify({
                "response": text,
                "type": "text"
            })

    except Exception as e:
        return jsonify({
            "error": f"{type(e).__name__}: {str(e)}",
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
    print("LUMO WEB MOCK MODE")
    print("="*60)
    print("Open browser to: http://localhost:5000")
    print("Type commands like: 'lumo what time is it'")
    print("="*60 + "\n")
    app.run(debug=False, port=5000)
