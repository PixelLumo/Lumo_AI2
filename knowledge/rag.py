"""RAG integration - inject knowledge into LLM prompts."""

from knowledge.search import retrieve


def answer_with_knowledge(user_input, messages, k=3):
    """
    Augment LLM call with retrieved knowledge.

    Args:
        user_input: User question
        messages: Existing message history (will be modified)
        k: Number of chunks to retrieve (default 3)

    Returns:
        Modified messages list with knowledge context injected
    """
    # Retrieve relevant chunks
    context_chunks = retrieve(user_input, k=k)

    if context_chunks:
        # Build knowledge block
        knowledge_block = "\n\n".join(context_chunks)

        # Inject as system message before user query
        messages.append({
            "role": "system",
            "content": f"Relevant knowledge from your knowledge base:\n\n{knowledge_block}"
        })

    # Add user query
    messages.append({
        "role": "user",
        "content": user_input
    })

    return messages


def answer_with_knowledge_verbose(user_input, messages, k=3):
    """
    Augment LLM call with retrieved knowledge (with metadata).

    Returns messages + source information.
    """
    from knowledge.search import retrieve_with_source

    results = retrieve_with_source(user_input, k=k)

    if results:
        # Build knowledge block with sources
        knowledge_parts = []
        for result in results:
            knowledge_parts.append(
                f"[From {result['source']}]\n{result['text']}"
            )
        knowledge_block = "\n\n".join(knowledge_parts)

        messages.append({
            "role": "system",
            "content": f"Relevant knowledge:\n\n{knowledge_block}"
        })

    messages.append({
        "role": "user",
        "content": user_input
    })

    return messages, results


# Example usage:
if __name__ == "__main__":
    # Test with sample query
    test_query = "How does the learning system work?"
    test_messages = []

    result = answer_with_knowledge(test_query, test_messages)
    print("Augmented messages:")
    for msg in result:
        print(f"\n{msg['role'].upper()}:")
        print(msg['content'][:200] + "...")
