# Security & Key Rotation

If you find a leaked API key (such as an OpenAI key) in this repository, follow these steps immediately:

1. Revoke the key in the provider dashboard (OpenAI):
   - Visit https://platform.openai.com/account/api-keys
   - Revoke/delete the exposed key.
2. Create a replacement key and store it securely (do not commit it).
3. Update your local `.env` (or environment variable) and restart services:

```powershell
# Set your OpenAI key in the environment; do NOT paste it into repository files.
# Example persistent command (PowerShell):
# setx OPENAI_API_KEY "<your-key-here>"
```

4. If the repo was pushed to a remote with the leaked key, purge it from history (see `scripts/purge_history.*`).
5. Rotate any other keys found and verify no further occurrences exist.

Use a secrets manager (Vault, AWS Secrets Manager, Azure Key Vault) in production.
