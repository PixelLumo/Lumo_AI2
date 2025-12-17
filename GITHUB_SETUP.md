# Lumo AI

A modular AI chat system with semantic search, local FAISS indexing, and OpenAI API fallback.

## Architecture

- **Framework**: Flask (Python web server)
- **Vector Store**: FAISS (Facebook AI Similarity Search) with semantic embeddings
- **Embeddings**: sentence-transformers "all-MiniLM-L6-v2" (384-dimensional vectors)
- **LLM**: Local FAISS search (primary) → OpenAI gpt-4o-mini (fallback)
- **Memory**: Pickle-based persistence for FAISS indices
- **Frontend**: HTML/CSS/JavaScript with simple textarea interface

## Project Structure

```
lumo-ai/
├── app/                    # Flask web server
│   ├── __init__.py
│   └── server.py          # POST /query endpoint
├── core/                   # Query orchestration
│   ├── __init__.py
│   ├── orchestrator.py    # Query handler
│   └── prompt_builder.py  # Prompt templates
├── models/                 # Intelligence layer
│   ├── __init__.py
│   └── model.py           # FAISS + OpenAI fallback
├── memory/                 # Persistence
│   ├── __init__.py
│   └── memory.py          # Save/load indices
├── tools/                  # Utilities
│   ├── __init__.py
│   └── tools.py
├── ui/                     # Frontend
│   ├── index.html
│   ├── app.js
│   └── style.css
├── run.py                  # Demo script
├── requirements.txt        # Dependencies
├── .env                    # Configuration
└── .gitignore
```

## Quick Start

### 1. Install Dependencies

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
OPENAI_API_KEY=your-api-key-here
LOCAL_MODEL=1
FAISS_DIM=384
FAISS_INDEX_PATH=memory/faiss_index.pkl
```

- `LOCAL_MODEL=1`: Use FAISS search (fast, local)
- `LOCAL_MODEL=0`: Use OpenAI API (powerful fallback)

### 3. Run Demo Script

```bash
python run.py
```

This adds example knowledge and queries the system:
```
Local FAISS hit: Python programming basics
```

### 4. Start Flask Server

```bash
python -c "import sys; sys.path.insert(0, '.'); from app.server import app; app.run(debug=True, port=5000)"
```

Or navigate to `ui/index.html` in a browser and interact with the web interface.

## API Endpoint

### POST /query

**Request:**
```json
{
  "prompt": "Tell me something about Python"
}
```

**Response:**
```json
{
  "response": "Local FAISS hit: Python programming basics"
}
```

## How It Works

1. **Query Received**: User sends prompt to `/query` endpoint
2. **Index Added**: Query is embedded and added to FAISS index
3. **Semantic Search**: FAISS searches for matching documents (local)
4. **Response Generated**: 
   - If FAISS has matches → Return best match
   - If no matches → Fall back to OpenAI API

## Dependencies

- **flask**: Web framework
- **faiss-cpu**: Vector similarity search
- **sentence-transformers**: Text embeddings (all-MiniLM-L6-v2)
- **numpy**: Array operations
- **requests**: HTTP client for OpenAI API
- **python-dotenv**: Environment configuration

## Testing

```bash
# Test demo script
python run.py

# Test Flask server (in separate terminal)
python -c "import sys; sys.path.insert(0, '.'); from app.server import app; app.run(port=5000)"

# Test API endpoint
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"hello world\"}"
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for fallback)
- `LOCAL_MODEL`: Set to `1` for FAISS-only, `0` for OpenAI-only
- `FAISS_DIM`: Embedding dimension (default: 384 for all-MiniLM-L6-v2)
- `FAISS_INDEX_PATH`: Path to save FAISS index (default: memory/faiss_index.pkl)

### Vector Store

- **Index Format**: FAISS IndexFlatL2 (Euclidean distance)
- **Embeddings**: 384-dimensional vectors from sentence-transformers
- **Persistence**: Pickled FAISS index + associated texts

## Future Enhancements

- [ ] Multi-turn conversation history
- [ ] Document ingestion pipeline
- [ ] Custom fine-tuning on domain-specific data
- [ ] WebSocket support for real-time streaming
- [ ] Advanced memory management (sliding window, summarization)
- [ ] Multiple LLM provider support (Anthropic, Cohere, etc.)

## License

MIT

## Author

Lumo AI Development Team
