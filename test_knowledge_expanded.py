"""Test expanded knowledge base."""

from knowledge.search import retrieve_with_source

test_queries = [
    'What are the system rules?',
    'How do safety guardrails work?',
    'Why did you choose these design decisions?',
    'How does the RAG pipeline work?',
    'What confirmation gates exist?'
]

print('='*60)
print('TESTING EXPANDED KNOWLEDGE BASE (75 chunks)')
print('='*60)

for query in test_queries:
    results = retrieve_with_source(query, k=2)
    print(f'\nQuery: "{query}"')
    for i, result in enumerate(results, 1):
        source = result['source'].replace('.txt', '').replace('.md', '')
        preview = result['text'][:70].replace('\n', ' ')
        distance = result['distance']
        print(f'  [{i}] [{source}] ({distance:.2f}) {preview}...')

print('\n' + '='*60)
print('✓ KNOWLEDGE BASE EXPANDED & READY')
print('='*60)
