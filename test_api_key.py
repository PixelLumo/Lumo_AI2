#!/usr/bin/env python3
"""Test OpenAI API authentication"""

from config.settings import OPENAI_API_KEY
import openai

print("="*60)
print("Testing OpenAI API Key")
print("="*60)

print(f"\nKey Length: {len(OPENAI_API_KEY)}")
print(f"Starts with 'sk-proj': {OPENAI_API_KEY.startswith('sk-proj')}")
print(
    f"Key preview: {OPENAI_API_KEY[:20]}..."
    f"{OPENAI_API_KEY[-10:]}"
)

try:
    openai.api_key = OPENAI_API_KEY

    # Try a simple API call
    response = openai.models.list()
    print("\n✓ API Key is VALID")
    print(f"  Available models: {len(response.data)}")

except Exception as e:
    print(f"\n✗ API Key FAILED: {e}")
    print("\nPossible issues:")
    print(
        "  1. Key is expired - create a new one at "
        "https://platform.openai.com/account/api-keys"
    )
    print(
        "  2. Account has no credits - check "
        "https://platform.openai.com/account/billing/overview"
    )
    print(
        "  3. Key has no permissions - regenerate from "
        "https://platform.openai.com/account/api-keys"
    )
