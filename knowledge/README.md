# Knowledge Subsystem

RAG knowledge base for LUMO AI.

## Structure

- **raw/** - Original documents, markdown, code files
- **chunks.jsonl** - Chunked text with metadata (one JSON per line)
- **index.faiss** - FAISS vector index for semantic search

## Format (chunks.jsonl)

```json
{"id": "chunk_0", "text": "...", "source": "file.md", "embedding": [...]}
```

## Usage

1. Add documents to `raw/`
2. Run chunking to populate `chunks.jsonl`
3. Build FAISS index from embeddings
4. Query index for RAG retrieval
