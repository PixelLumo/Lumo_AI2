# Lumo_AI Web Assistant

## Setup

1. Create a virtual environment:

2. Add a `.env` file to the project root with your OpenAI key:

```text
OPENAI_API_KEY=sk-<your-key-here>
```

Do NOT commit `.env` to version control; it is included in `.gitignore`.

Setup pre-commit and secret scanning (recommended):

```bash
pip install pre-commit detect-secrets
# initialize a git repo if you haven't already
git init
# create a baseline of existing findings (review it before committing)
detect-secrets scan > .secrets.baseline
# install pre-commit hooks
pre-commit install
# run hooks across all files
pre-commit run --all-files
```

If you find any real secrets, rotate them immediately and remove them from history (see below).

