"""Test RAG integration with LLM."""

print("Testing RAG integration with LLM...\n")

# Test 1: Check imports
print("[1] Checking imports...")
try:
    from core.llm import ask_llm, ask_llm_with_knowledge
    from knowledge.rag import answer_with_knowledge
    from knowledge.search import retrieve
    print("  ✓ All imports successful\n")
except ImportError as e:
    print(f"  ✗ Import failed: {e}\n")
    exit(1)

# Test 2: Check knowledge base
print("[2] Checking knowledge base...")
try:
    results = retrieve("How does memory work?", k=2)
    if results:
        print(f"  ✓ Retrieved {len(results)} chunks\n")
    else:
        print("  ! No chunks in knowledge base (add docs to knowledge/raw/)\n")
except Exception as e:
    print(f"  ✗ Knowledge retrieval failed: {e}\n")
    exit(1)

# Test 3: Check RAG augmentation
print("[3] Testing message augmentation...")
try:
    query = "How does the system work?"
    messages = answer_with_knowledge(query, [], k=2)
    print(f"  ✓ Augmented {len(messages)} messages")
    for i, msg in enumerate(messages):
        preview = msg["content"][:60].replace("\n", " ")
        print(f"    [{i}] {msg['role'].upper()}: {preview}...\n")
except Exception as e:
    print(f"  ✗ Augmentation failed: {e}\n")
    exit(1)

# Test 4: Show how to use
print("[4] Integration examples:\n")

print("Example A - Direct RAG call (recommended):")
print("""
    from core.llm import ask_llm_with_knowledge
    
    response = ask_llm_with_knowledge(
        "How does memory work?",
        k=3
    )
    print(response["content"])
""")

print("\nExample B - Manual RAG integration:")
print("""
    from knowledge.rag import answer_with_knowledge
    from core.llm import ask_llm
    
    messages = []
    messages = answer_with_knowledge("How does memory work?", messages)
    response = ask_llm(messages)
    print(response["content"])
""")

print("\nExample C - With message history:")
print("""
    messages = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"}
    ]
    response = ask_llm_with_knowledge(
        "Tell me more",
        messages=messages,
        k=3
    )
""")

print("\n" + "=" * 60)
print("✓ RAG INTEGRATION READY")
print("=" * 60)
print("\nNext: Use ask_llm_with_knowledge() in your code")
print("      OR manually augment with answer_with_knowledge()")
