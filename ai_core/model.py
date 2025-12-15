import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# NOTE: Don't read or validate the OpenAI API key at import time; do it lazily
# inside `handle_query` so the app can start even when the key isn't set.

def handle_query(prompt: str) -> str:
    """
    Sends a user prompt to OpenAI and returns the AI's response.
    Returns a friendly message if something goes wrong.
    """
    if not prompt:
        return "Please enter a question."

    # Ensure API key is available at request time
    api_key = os.getenv("OPENAI_API_KEY")
    # Treat placeholders or unset values as missing keys
    if (
        not api_key
        or api_key.strip() == ""
        or api_key.upper().startswith("YOUR")
        or "PLACEHOLDER" in api_key.upper()
    ):
        return (
            "OpenAI API key not set or is a placeholder. Please set a valid "
            "OPENAI_API_KEY environment variable or add it to a .env file."
        )

    # Instantiate the OpenAI client with the API key for this request
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        # New SDK returns a similar structure; extract the assistant message
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error querying AI: {e}"
# Example usage
if __name__ == "__main__":
    user_prompt = "What is the capital of France?"
    print(handle_query(user_prompt))