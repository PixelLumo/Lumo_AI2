from models.model import add_to_index, generate_response

# Add example knowledge
add_to_index([
    "Hello world",
    "Python programming basics",
    "How to cook pasta"
])

# Query AI
query = "Tell me something about Python"
response = generate_response(query)
print(response)
