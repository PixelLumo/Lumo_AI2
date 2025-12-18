def semantic_search(query: str, top_k: int = 5):
    # Return dummy results
    return [f"Dummy result {i+1} for query '{query}'" for i in range(top_k)]
    """
    Retrieve top-k relevant chunks from knowledge base.

    Args:
        query: User question or search term
        k: Number of chunks to return (default 3)

    Returns:
        List of relevant chunk texts
    """
    if not READY:
        return []

    # Encode query
    q_emb = MODEL.encode(query).astype("float32")

    # Search index
    distances, indices = index.search(np.array([q_emb]), k)

    # Return chunk texts
    results = [CHUNKS[i]["text"] for i in indices[0] if i < len(CHUNKS)]
    return results


def retrieve_with_source(query, k=3):
    """
    Retrieve chunks with source metadata.

    Args:
        query: User question or search term
        k: Number of chunks to return (default 3)

    Returns:
        List of dicts with 'text' and 'source'
    """
    if not READY:
        return []

    q_emb = MODEL.encode(query).astype("float32")
    distances, indices = index.search(np.array([q_emb]), k)

    results = []
    for i in indices[0]:
        if i < len(CHUNKS):
            results.append({
                "text": CHUNKS[i]["text"],
                "source": CHUNKS[i].get("source", "unknown"),
                "distance": float(distances[0][indices[0].tolist().index(i)])
            })
    return results
