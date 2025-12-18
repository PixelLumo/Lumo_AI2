# 🎮 LUMO Command Cheat Sheet

## All Available Commands (Copy & Paste)

---

## ⏰ Time Commands

```
lumo what time is it
lumo tell me the time
lumo current time
```

**Response:** Current time in 12-hour format (e.g., "02:45 PM")

---

## 🌤️ Weather Commands

### New York (Default)
```
lumo weather in new york
lumo weather
lumo new york weather
```

### London
```
lumo weather in london
lumo london weather
```

### Tokyo
```
lumo weather in tokyo
lumo weather tokyo
```

### San Francisco
```
lumo weather in san francisco
lumo san francisco weather
```

### Sydney
```
lumo weather in sydney
lumo sydney weather
```

---

## 🧮 Calculator Commands

### Simple Math
```
lumo calculate 10 + 5
lumo calculate 100 - 50
lumo calculate 20 * 3
lumo calculate 100 / 4
```

### With Parentheses
```
lumo calculate (10 + 5) * 2
lumo calculate (100 - 50) / 2
lumo calculate 10 + 5 * 2
lumo calculate (20 * 5) - 10
```

### Alternative Syntax
```
lumo 10 + 5
lumo math 50 * 2
lumo calculate 75 / 3
```

---

## 📝 Note Management

### Save a Note
```
lumo save my project ideas
lumo save important meeting notes
lumo note my thoughts
lumo save remember this
```

**Then confirm with:**
```
yes
confirm
ok
```

**Or reject with:**
```
no
cancel
stop
```

### List All Notes
```
lumo list notes
lumo show my notes
lumo list notes please
```

### Delete Oldest Note
```
lumo delete note
lumo delete a note
lumo remove note
```

---

## 🔍 Web Search

```
lumo search for machine learning
lumo search artificial intelligence
lumo search python programming
lumo search for the latest news
```

---

## 💬 Conversation

### Greetings
```
lumo hello
lumo hi
lumo hey
```

**Response:** "Hello! I'm LUMO. You have X saved notes. How can I help?"

### About LUMO
```
lumo tell me about yourself
lumo what's your name
lumo who are you
lumo about lumo
```

### Get Help
```
lumo help
lumo show me commands
lumo what can you do
```

---

## 🎯 Example Conversations

### Conversation 1: Time & Notes
```
You:   "lumo hello"
LUMO:  "Hello! I'm LUMO. You have 0 saved notes. How can I help?"

You:   "lumo what time is it"
LUMO:  "The current time is 02:45 PM"

You:   "lumo save my meeting at 3 PM"
LUMO:  "Save note with content: 'my meeting at 3 PM'. Say 'yes' to confirm."

You:   "yes"
LUMO:  "Note saved."

You:   "lumo list notes"
LUMO:  "Your notes:
        • my meeting at 3 PM"
```

### Conversation 2: Weather & Calculator
```
You:   "lumo weather in london"
LUMO:  "Weather in London: 42°F, Rainy, 80% humidity"

You:   "lumo calculate 50 * 2"
LUMO:  "50 * 2 = 100"

You:   "lumo help"
LUMO:  "Available commands:
        • 'lumo what time is it' - Get current time
        • 'lumo search for X' - Search the web
        ..."
```

### Conversation 3: Notes & Cleanup
```
You:   "lumo save project idea 1"
LUMO:  "Save note with content: 'project idea 1'. Say 'yes' to confirm."

You:   "yes"
LUMO:  "Note saved."

You:   "lumo save project idea 2"
LUMO:  "Save note with content: 'project idea 2'. Say 'yes' to confirm."

You:   "yes"
LUMO:  "Note saved."

You:   "lumo list notes"
LUMO:  "Your notes:
        • project idea 1
        • project idea 2"

You:   "lumo delete note"
LUMO:  "Oldest note deleted."

You:   "lumo list notes"
LUMO:  "Your notes:
        • project idea 2"
```

---

## ⚡ Quick Actions (Sidebar Buttons)

Click these buttons instead of typing:

| Button | Command | What It Does |
|--------|---------|--------------|
| 🕐 Current Time | `lumo what time is it` | Shows current time |
| 🌤️ Weather | `lumo weather in new york` | Shows NYC weather |
| 🔍 Search Web | `lumo search for AI` | Search example |
| 🧮 Math | `lumo calculate 10 + 5 * 2` | Math example |
| 📝 List Notes | `lumo list notes` | Show all notes |
| ❓ Help | `lumo help` | Show commands |

---

## 🎨 UI Elements

### Message Types
- **Blue (Right):** Your message
- **Purple (Left):** LUMO's response
- **Yellow:** System information
- **Red:** Error message
- **Green:** Action result

### Indicators
- **Status:** Shows Ready/Thinking/Error
- **Counter:** Total messages sent/received
- **Loading:** Spinning dots while processing
- **Clear Chat:** Button to reset conversation

---

## 🔄 Confirmation Flow Example

```
1. You ask to save: "lumo save my ideas"
2. LUMO asks: "Save note with content: 'my ideas'. Say 'yes' to confirm."
3. You can:
   ✅ Confirm: "yes", "confirm", "ok"
   ❌ Reject: "no", "cancel", "stop"
   ⏳ Wait: Type anything else to keep asking
```

---

## 🚫 Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| "what time is it" | ❌ Missing wake word → ✅ "lumo what time is it" |
| "lumo serch for AI" | ❌ Typo → ✅ "lumo search for AI" |
| "lumo save my notes" / "yes" | ❌ No confirmation message → ✅ See confirmation prompt first |
| "lumo calculate a + b" | ❌ Letters in math → ✅ "lumo calculate 10 + 5" |
| "lumo weather" | ✅ Uses default (New York) - OK |
| Just typing "hello" | ❌ No wake word → ✅ "lumo hello" |

---

## 💾 Data Storage

### Where Notes Are Saved
- **File:** `data/notes.json`
- **Format:** JSON array
- **Persists:** Yes (survives restarts)
- **Max Notes:** Unlimited

### Example File Content
```json
[
  {
    "content": "my project ideas",
    "timestamp": "2025-12-18T02:45:30.123456"
  },
  {
    "content": "meeting at 3 PM",
    "timestamp": "2025-12-18T02:46:15.789012"
  }
]
```

---

## ⚙️ Advanced Usage

### Combining Commands
```
lumo search for information then save results
→ Searches (first pattern match wins)

lumo weather in london and new york
→ Shows London weather (first match)
```

### Math with Different Operators
```
lumo calculate 10 + 5 - 2              (= 13)
lumo calculate 2 * 3 + 4               (= 10)
lumo calculate 100 / 2 + 25            (= 75)
lumo calculate (10 + 5) * (2 + 3)      (= 75)
```

### Multiple Word Searches
```
lumo search for artificial intelligence and machine learning
→ Searches for: "artificial intelligence and machine learning"

lumo search machine learning Python
→ Searches for: "machine learning Python"
```

---

## 🎓 Tips & Tricks

1. **Use Quick Buttons:** Click sidebar buttons instead of typing
2. **Short Messages:** "lumo calculate 10 + 5" is faster than "please calculate 10 plus 5"
3. **Default City:** "lumo weather" = New York weather
4. **Clear Chat:** Use "Clear Chat" button to reset conversation
5. **Note Management:** Always check "lumo list notes" before deleting
6. **Math Validation:** Only numbers and `+`, `-`, `*`, `/`, `(` `)` allowed

---

## 🔗 Links & Resources

- **Server:** http://localhost:5000
- **Documentation:** See FEATURES_ENHANCED.md
- **Pattern Reference:** See MOCK_LLM_PATTERNS.md
- **Logs:** Check lumo.log for text logs

---

## 📋 Feature Checklist

- ✅ Time responses (current time)
- ✅ Weather (5 cities)
- ✅ Calculator (all operators)
- ✅ Notes (save, list, delete)
- ✅ Web search (function calls)
- ✅ Help system
- ✅ Greeting
- ✅ About message
- ✅ Confirmation flow
- ✅ Status indicators
- ✅ Message counter
- ✅ Clear chat

---

**Need more help?** Type `lumo help` in the chat!

