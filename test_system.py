#!/usr/bin/env python3
"""Integration test - test all components together."""

from core.memory import Memory
from core.llm import generate_response
from knowledge.search import semantic_search

def test_system():
    print("Testing system integration...")
    
    # Test memory
    mem = Memory()
    mem.add("Hi", "Hello!")
    assert len(mem.get_context()) > 0
    
    # Test LLM
    response = generate_response("What is your name?", mem)
    assert len(response) > 0
    
    # Test knowledge
    results = semantic_search("test")
    assert len(results) > 0
    
    print("✓ System integration test PASSED")

if __name__ == "__main__":
    test_system()
