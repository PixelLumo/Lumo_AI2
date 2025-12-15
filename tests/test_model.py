import os

from ai_core.model import handle_query


def test_handle_query_no_key():
    # Ensure behavior when no API key is set
    original = os.environ.pop("OPENAI_API_KEY", None)
    try:
        resp = handle_query("Hello")
        assert "OpenAI API key not set" in resp or "placeholder" in resp
    finally:
        if original is not None:
            os.environ["OPENAI_API_KEY"] = original


def test_handle_query_placeholder_key():
    original = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
    try:
        resp = handle_query("Hello")
        assert "OpenAI API key not set" in resp or "placeholder" in resp
    finally:
        if original is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = original
