def listen_for_speech() -> bytes:
    # Dummy microphone capture
    input_text = input("You (simulating voice input): ")
    if input_text.strip() == "":
        return None
    return input_text.encode()
