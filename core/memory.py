class Memory:
    def __init__(self):
        self.history = []

    def add(self, user_text: str, ai_text: str):
        self.history.append({"user": user_text, "ai": ai_text})
        if len(self.history) > 20:  # keep last 20 interactions
            self.history.pop(0)

    def get_context(self) -> str:
        return "\n".join(
            [f"User: {item['user']}\nLumo: {item['ai']}" for item in self.history]
        )
