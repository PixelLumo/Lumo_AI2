"""End-to-end RAG pipeline test."""

import os
import sys

# Test 1: Check knowledge subsystem exists
print("=" * 60)
print("TESTING RAG PIPELINE")
print("=" * 60)

print("\n[1] Checking knowledge subsystem...")
required_dirs = ["knowledge", "knowledge/raw"]
for d in required_dirs:
    if os.path.isdir(d):
        print(f"  ✓ {d}/")
    else:
        print(f"  ✗ {d}/ MISSING")
        sys.exit(1)

# Test 2: Create sample documents
print("\n[2] Creating sample documents...")
sample_docs = {
    "memory.txt": """
The LUMO memory system uses FAISS (Facebook AI Similarity Search) for vector embeddings.
It stores conversation history in a FAISS index for fast semantic retrieval.
Memory embeddings are 768-dimensional vectors from sentence transformers.
You can search past conversations by semantic similarity, not just keywords.
Memory is persistent in memory/conversation_history.json.
""",
    "learning.txt": """
The learning module tracks interaction patterns and provides improvement suggestions.
It analyzes wake word detection, success rates, and identifies failure patterns.
Learning data is stored in learning logs for continuous improvement.
The system can auto-tune thresholds based on historical performance.
Learning insights help LUMO become smarter over time.
""",
    "actions.txt": """
LUMO supports three main action types: web_search, save_note, and execute_action.
Destructive actions like save_note require explicit user confirmation.
Read-only actions like web_search execute immediately without confirmation.
Actions are logged with arguments and results for debugging and learning.
The action executor validates inputs and handles errors gracefully.
"""
}

for fname, content in sample_docs.items():
    path = f"knowledge/raw/{fname}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ Created {path}")

# Test 3: Run ingest
print("\n[3] Ingesting documents...")
try:
    from knowledge.ingest import ingest
    ingest()
    print("  ✓ Chunks created")
except Exception as e:
    print(f"  ✗ Ingest failed: {e}")
    sys.exit(1)

# Test 4: Build index
print("\n[4] Building FAISS index...")
try:
    import json
    import numpy as np
    import faiss
    from sentence_transformers import SentenceTransformer

    MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = []
    embeddings = []

    with open("knowledge/chunks.jsonl", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            chunks.append(obj)

    print(f"  Encoding {len(chunks)} chunks...")
    embeddings = [MODEL.encode(obj["text"]) for obj in chunks]
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "knowledge/index.faiss")

    with open("knowledge/metadata.jsonl", "w", encoding="utf-8") as f:
        for obj in chunks:
            f.write(json.dumps(obj) + "\n")

    print(f"  ✓ Index built ({len(chunks)} chunks)")
except Exception as e:
    print(f"  ✗ Indexing failed: {e}")
    sys.exit(1)

# Test 5: Query the index
print("\n[5] Testing retrieval...")
test_queries = [
    "How does memory work?",
    "What learning features exist?",
    "Tell me about actions"
]

try:
    from knowledge.search import retrieve

    for query in test_queries:
        results = retrieve(query, k=2)
        print(f"\n  Query: '{query}'")
        for i, chunk in enumerate(results, 1):
            preview = chunk[:80].replace("\n", " ")
            print(f"    [{i}] {preview}...")
except Exception as e:
    print(f"  ✗ Retrieval failed: {e}")
    sys.exit(1)

# Test 6: RAG integration
print("\n[6] Testing RAG augmentation...")
try:
    from knowledge.rag import answer_with_knowledge

    user_input = "How do I use the memory system?"
    messages = []

    augmented = answer_with_knowledge(user_input, messages, k=2)

    print(f"\n  Augmented messages ({len(augmented)} messages):")
    for i, msg in enumerate(augmented):
        role = msg["role"].upper()
        content_preview = msg["content"][:100].replace("\n", " ")
        print(f"    [{i}] {role}: {content_preview}...")
except Exception as e:
    print(f"  ✗ RAG failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ RAG PIPELINE WORKING")
print("=" * 60)
print("\nNext steps:")
print("  1. Add more documents to knowledge/raw/")
print("  2. Run: python test_rag.py")
print("  3. Integrate with: from knowledge.rag import answer_with_knowledge")
print("  4. Use in LLM calls: messages = answer_with_knowledge(query, messages)")
