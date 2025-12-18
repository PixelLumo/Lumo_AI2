def save_note(content):
    with open("notes.txt", "a") as f:
        f.write(content + "\n")
    return "Note saved."
