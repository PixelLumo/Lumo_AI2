# Mock LLM Pattern Matching Reference

## Overview

`web_app_mock.py` uses keyword-based pattern matching to simulate LLM responses without API calls. This document explains how each pattern works.

## Pattern Matching Rules

### 1. Search Pattern
**Keywords:** `"search"` in message

```python
if "search" in user_msg:
    query = user_msg.replace("search", "").replace("for", "").strip()
    # Returns function call to web_search
```

**Examples:**
```
"lumo search for python" → query = "python"
"lumo search machine learning" → query = "machine learning"
"lumo search the web for AI" → query = "the web AI"
```

### 2. Save Note Pattern
**Keywords:** `"save"` OR `"note"` in message

```python
elif "save" in user_msg or "note" in user_msg:
    content = user_msg.replace("save", "").replace("my", "").strip()
    # Returns function call to save_note
    # Requires confirmation (destructive action)
```

**Examples:**
```
"lumo save my project ideas" → content = "project ideas"
"lumo note about the meeting" → content = "about the meeting"
"lumo save important" → content = "important"
```

### 3. List Notes Pattern
**Keywords:** `"list"` AND `"note"` in message

```python
elif "list" in user_msg and "note" in user_msg:
    # Loads from data/notes.json
    # Returns all notes as formatted list
```

**Examples:**
```
"lumo list notes" → Shows all saved notes
"lumo list my notes" → Shows all saved notes
```

### 4. Delete Note Pattern
**Keywords:** `"delete"` AND `"note"` in message

```python
elif "delete" in user_msg and "note" in user_msg:
    # Deletes oldest note from data/notes.json
    # Saves back to disk
```

**Examples:**
```
"lumo delete note" → Deletes oldest note
"lumo delete a note" → Deletes oldest note
```

### 5. Weather Pattern
**Keywords:** `"weather"` OR `"temperature"` in message

```python
elif "weather" in user_msg or "temperature" in user_msg:
    location = "new york"  # default
    for city in WEATHER_DATA.keys():
        if city in user_msg:
            location = city
    # Returns formatted weather string
```

**Available Cities:**
- new york
- san francisco
- london
- tokyo
- sydney

**Examples:**
```
"lumo weather in london" → Location = "london"
"lumo what's the weather" → Location = "new york" (default)
"lumo temperature in tokyo" → Location = "tokyo"
```

### 6. Calculator Pattern
**Keywords:** `"+", "-", "*", "/"` in message OR `"calculate"` OR `"math"`

```python
elif any(op in user_msg for op in ["+", "-", "*", "/"]) or \
     "calculate" in user_msg or "math" in user_msg:
    expr = user_msg.replace("calculate", "").replace("math", "").strip()
    result = evaluate_math(expr)
    # Returns "expression = result"
```

**Safe Evaluation:**
Only allows: `0-9`, `+`, `-`, `*`, `/`, `(`, `)`, space

**Examples:**
```
"lumo calculate 10 + 5" → "10 + 5 = 15"
"lumo 50 * 2" → "50 * 2 = 100"
"lumo math (10 + 5) * 2" → "(10 + 5) * 2 = 30"
```

### 7. Time Pattern
**Keywords:** `"time"` in message

```python
elif "time" in user_msg:
    return {
        "content": f"The current time is {datetime.now().strftime('%I:%M %p')}",
        "function_call": None
    }
```

**Examples:**
```
"lumo what time is it" → "The current time is 02:30 PM"
"lumo tell me the time" → "The current time is 02:30 PM"
```

### 8. Greeting Pattern
**Keywords:** `"hello"` OR `"hi"` OR `"hey"` in message

```python
elif "hello" in user_msg or "hi" in user_msg or "hey" in user_msg:
    notes_count = len(load_notes())
    return {
        "content": f"Hello! I'm LUMO. You have {notes_count} saved notes. How can I help?",
        "function_call": None
    }
```

**Examples:**
```
"lumo hello" → Greeting with note count
"lumo hi there" → Greeting with note count
```

### 9. About Pattern
**Keywords:** `"name"` OR `"yourself"` OR `"about"` in message

```python
elif "name" in user_msg or "yourself" in user_msg or "about" in user_msg:
    return {
        "content": "I'm LUMO, your AI assistant. I can:\n• Search the web\n• ...",
        "function_call": None
    }
```

**Examples:**
```
"lumo what's your name" → Full capabilities list
"lumo tell me about yourself" → Full capabilities list
```

### 10. Help Pattern
**Keywords:** `"help"` OR `"commands"` in message

```python
elif "help" in user_msg or "commands" in user_msg:
    return {
        "content": "Available commands:\n• 'lumo what time is it'\n• ...",
        "function_call": None
    }
```

**Examples:**
```
"lumo help" → Lists all commands
"lumo show me commands" → Lists all commands
```

### 11. Default Pattern
**No keywords match**

```python
else:
    return {
        "content": f"I heard: '{user_msg}'. Try 'lumo help' for available commands.",
        "function_call": None
    }
```

## Function Routing

### Destructive Actions (Require Confirmation)
```python
DESTRUCTIVE_ACTIONS = {
    "save_note": True,    # Requires yes/no
    "web_search": False   # No confirmation needed
}
```

**Confirmation Flow:**
1. User: "lumo save my notes"
2. LUMO: "Save note with content: 'my notes'. Say 'yes' to confirm."
3. User: "yes"
4. LUMO: "Note saved."

**Rejection Flow:**
1. User: "lumo save my notes"
2. LUMO: "Save note with content: 'my notes'. Say 'yes' to confirm."
3. User: "no"
4. LUMO: "Action cancelled."

## Response Structure

All responses follow this format:

```python
{
    "content": "The text response",
    "function_call": None  # or {...}
}
```

### Text Response
```python
{
    "content": "The current time is 02:30 PM",
    "function_call": None
}
```

### Function Call Response
```python
{
    "content": "",
    "function_call": {
        "name": "web_search",
        "arguments": '{"query": "python"}'
    }
}
```

## Storage

### Persistent Notes
- **File:** `data/notes.json`
- **Format:** JSON array of note objects
- **Structure:** `[{"content": "...", "timestamp": "..."}, ...]`
- **Auto-created:** `data/` directory created on first run

### Weather Data
- **Storage:** In-memory dictionary
- **Data:** 5 pre-populated cities
- **Updates:** None (static mock data)

## Error Handling

### Calculator Errors
- Invalid syntax → "Invalid calculation"
- Non-number characters → Safely rejected
- Division by zero → Safe (Python eval handles)

### Notes Errors
- No notes to list → "You have no saved notes yet."
- No notes to delete → "No notes to delete."
- File corruption → Falls back to empty array

### File I/O
- Missing `data/notes.json` → Created automatically
- Missing `data/` folder → Created automatically
- Corruption → Caught with try/except

## Testing Patterns

### Complete Flow Test
```
1. "lumo hello" → Greeting
2. "lumo what time is it" → Current time
3. "lumo search for python" → Function call
4. "lumo save my idea" → Confirmation request
5. "yes" → Saved
6. "lumo list notes" → Show notes
7. "lumo weather in london" → Weather data
8. "lumo calculate 100 + 50" → Math result
9. "lumo help" → Commands list
10. "lumo delete note" → Delete oldest
```

### Edge Cases
- Empty query: "lumo" alone → Wake word detected but no query
- Missing wake word: "hello" → Rejected
- Typos: "lumo serch" → Default response
- Mixed case: "LUMO Weather" → Works (case-insensitive)
- Multiple keywords: "lumo weather and time" → Matches first pattern (weather)

## Extending Patterns

### Adding New Pattern
1. Add condition to `mock_ask_llm()`
2. Test with sample input
3. Document in this file
4. Update help text

### Example: Adding "joke" pattern
```python
elif "joke" in user_msg:
    jokes = [
        "Why did the AI go to school? To improve its learning!",
        "What do you call an AI that tells jokes? Artificial funny!",
    ]
    import random
    return {
        "content": random.choice(jokes),
        "function_call": None
    }
```

## Performance Notes

- **Pattern matching:** O(1) for each keyword check
- **Note loading:** O(n) where n = number of notes
- **No API calls:** All responses generated instantly
- **Memory efficient:** Stores only note content and timestamp

