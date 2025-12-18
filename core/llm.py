import requests
import json
from core.memory import Memory

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.1"

def generate_response(prompt: str, memory: Memory) -> str:
    # Include memory context
    context = memory.get_context()
    full_prompt = f"{context}\nUser: {prompt}\nLumo:"
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": full_prompt, "stream": False},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        return data.get("completion", "Sorry, I could not respond.")
    except Exception as e:
        return f"LLM Error: {e}"

