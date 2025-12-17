from models.model import generate_response, add_to_index


def handle_query(user_input):
    # Add user input to memory
    add_to_index([user_input])
    # Generate AI response
    return generate_response(user_input)
