#!/usr/bin/env python3
"""Test knowledge search."""

from knowledge.search import semantic_search

def test_knowledge():
    results = semantic_search("What is the system?")
    assert len(results) > 0
    print(f"✓ Knowledge test PASSED - found {len(results)} results")

if __name__ == "__main__":
    test_knowledge()
