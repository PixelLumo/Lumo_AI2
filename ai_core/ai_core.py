from .model import handle_query as generate_response
from .memory import load_memory, save_memory
from .web_agent import search_web

memory = load_memory()

def handle_query(prompt):
    if prompt in memory:
        return memory[prompt]

    if "search" in prompt.lower():
        response = search_web(prompt)
    else:
        response = generate_response(prompt)

    memory[prompt] = response
    save_memory(memory)
    return response
