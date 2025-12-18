import json

def log_interaction(user_text: str, ai_text: str):
    entry = {"user": user_text, "ai": ai_text}
    with open("learning_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")
    print("[Logger] Interaction logged.")

