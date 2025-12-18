import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

LLM_MODEL = "gpt-4o"
VOICE_NAME = "Jarvis"
MEMORY_PATH = "memory.faiss"
