def save_note(text: str):
    with open("notes.txt", "a") as f:
        f.write(text + "\n")
    return "Note saved."
