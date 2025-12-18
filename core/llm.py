import requests
from knowledge.rag import answer_with_knowledge

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1"

SYSTEM_PROMPT = """
You are LUMO, a JARVIS-style AI assistant.
You are concise, intelligent, and efficient.
You decide whether to speak or execute an action.
If no clear intent exists, stay silent.
"""


def ask_llm(messages):
    """
    Send messages to Ollama LLM

    Args:
        messages: List of message dicts with role and content

    Returns:
        dict with 'content' field
    """
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        "stream": False
    }

    print(f"[DEBUG_OLLAMA] Sending payload: {payload}")

    r = requests.post(OLLAMA_URL, json=payload, timeout=60)

    print(f"[DEBUG_OLLAMA] Response status: {r.status_code}")
    print(f"[DEBUG_OLLAMA] Response text: {r.text}")

    r.raise_for_status()

    return {"content": r.json()["message"]["content"]}


def ask_llm_with_knowledge(query, messages=None, k=3):
    """
    Send query to LLM with retrieved knowledge context.

    This is the RAG-augmented version - retrieves relevant chunks
    from the knowledge base and injects them as system context.

    Args:
        query: User question or prompt
        messages: Optional message history (default: empty)
        k: Number of knowledge chunks to retrieve (default: 3)

    Returns:
        dict with 'content' field
    """
    if messages is None:
        messages = []

    # Augment messages with knowledge
    messages = answer_with_knowledge(query, messages.copy(), k=k)

    return ask_llm(messages)

