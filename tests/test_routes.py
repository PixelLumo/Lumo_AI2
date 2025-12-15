import json
from unittest.mock import patch

from app import create_app


def fake_chat_completion_create(model, messages, max_tokens, temperature):
    class Msg:
        pass

    class Choice:
        def __init__(self):
            self.message = Msg()

    choice = Choice()
    choice.message.content = "Hello from fake AI"
    return type("Resp", (), {"choices": [choice]})


def test_ask_endpoint(monkeypatch):
    app = create_app()
    client = app.test_client()
    # Set a non-placeholder API key so `handle_query` proceeds to create the client
    monkeypatch.setenv("OPENAI_API_KEY", "FAKE_VALID_KEY")

    # Patch OpenAI client creation to avoid real API calls
    with patch("ai_core.model.OpenAI") as MockOpenAI:
        mock_instance = MockOpenAI.return_value
        mock_instance.chat.completions.create.side_effect = fake_chat_completion_create

        resp = client.post("/ask", json={"prompt": "Hello"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert "response" in data and "Hello from fake AI" in data["response"]
