# LUMO AI - Complete File Understanding

## Summary
✅ **Status: All modules working**
- ✓ All imports successful
- ✓ All functions callable
- ✓ No breaking errors
- ✓ Ready to run (will block on audio input)

---

## File Breakdown

### 1. **config/settings.py** - Configuration Hub
```
PURPOSE: Single source of truth for all settings
IMPORTS: os, dotenv
KEY DATA:
  - OPENAI_API_KEY: From .env
  - ELEVENLABS_API_KEY: From .env
  - LLM_MODEL: "gpt-4o" (hardcoded)
  - VOICE_NAME: "Jarvis" (ElevenLabs voice ID)
  - MEMORY_PATH: "memory.faiss" (for future use)
```

**How it works:**
1. Loads `.env` file at startup
2. Extracts API keys from environment
3. Sets defaults (LLM_MODEL, VOICE_NAME)
4. Other modules import from here

---

### 2. **core/llm.py** - The Brain
```
PURPOSE: Interface to OpenAI GPT-4o with function calling
IMPORTS: openai.OpenAI, config.settings
KEY COMPONENTS:
  - client: OpenAI API client (initialized with API key)
  - SYSTEM_PROMPT: 191 chars defining LUMO's personality
  - ask_llm(): Main function for LLM interaction
```

**ask_llm() function:**
- **Input:** 
  - `messages`: List of {role, content} dicts
  - `functions`: Optional list of function definitions
- **Logic:**
  1. Build payload with model, messages, optionally functions
  2. Call `client.chat.completions.create()`
  3. Extract message from response
  4. Return dict with:
     - `content`: Text response (or empty string)
     - `function_call`: {name, arguments} if function was called
- **Output:** Dict with content and/or function_call

**Key Detail:** Returns function_call as:
```python
{
  "name": "web_search",
  "arguments": '{"query": "python"}' # JSON string from OpenAI
}
```

---

### 3. **core/memory.py** - Context Engine
```
PURPOSE: FAISS-based semantic search for context
IMPORTS: faiss, numpy
KEY CLASS: Memory(dim=1536)
```

**Memory class:**
- **__init__(dim=1536):**
  - Creates FAISS IndexFlatL2 (L2 distance metric)
  - Initializes empty data list

- **add(embedding, text):**
  - Takes 1536-dim embedding vector
  - Adds to FAISS index
  - Stores corresponding text

- **search(embedding, k=3):**
  - Takes query embedding
  - Returns k nearest text matches
  - Returns [] if index empty

**Current State:** Not used in run.py yet, ready for expansion

---

### 4. **core/planner.py** - Action Router
```
PURPOSE: Routes function calls to actual implementations
IMPORTS: json, actions.web_search, actions.notes
KEY FUNCTION: execute_action(name, arguments)
```

**execute_action() logic:**
1. **Argument parsing:**
   - Checks if arguments is JSON string
   - Parses with `json.loads()`
   - Falls back to {} on parse error
   
2. **Action routing:**
   - "web_search" → `web_search(args["query"])`
   - "save_note" → `save_note(args["content"])`
   - Anything else → "Action not implemented."

**Important:** Handles both JSON string and dict arguments
(OpenAI sends JSON strings in function_call.arguments)

---

### 5. **audio/stt.py** - Whisper Input
```
PURPOSE: Record audio and transcribe to text
IMPORTS: openai, sounddevice, numpy, tempfile, scipy.io.wavfile
KEY FUNCTION: listen(seconds=5)
```

**listen() flow:**
1. **Record audio:**
   - Sample rate: 16000 Hz
   - Duration: 5 seconds (default)
   - Mono (1 channel)
   - Uses sounddevice.rec()
   - Prints "Listening..."

2. **Process audio:**
   - Create temp .wav file
   - Convert float audio to int16
   - Save to temp file

3. **Transcribe:**
   - Set openai.api_key from config
   - Send to Whisper API
   - Return transcript.text

4. **Error handling:**
   - Try/except wrapper
   - Prints error message
   - Returns empty string on failure

---

### 6. **audio/tts.py** - ElevenLabs Output
```
PURPOSE: Text-to-speech via ElevenLabs API
IMPORTS: requests, config.settings
KEY FUNCTION: speak(text)
```

**speak() flow:**
1. **Validation:**
   - Check if ELEVENLABS_API_KEY is set
   - Return False if not set

2. **API call:**
   - URL: `https://api.elevenlabs.io/v1/text-to-speech/{VOICE_NAME}`
   - Headers: xi-api-key and Content-Type
   - Data: text + voice settings (stability 0.4, similarity 0.8)

3. **Response handling:**
   - Status 200 → Save to response.mp3
   - Other status → Print error
   - Return True/False

4. **Error handling:**
   - Try/except wrapper
   - Returns False on exception

---

### 7. **actions/web_search.py** - Search Stub
```
PURPOSE: Handle web search function calls (stub)
IMPORTS: none
KEY FUNCTION: web_search(query)
```

**Current implementation:**
- Returns: `f"I would search the web for: {query}"`
- Status: STUB (not implemented)
- Ready for: Real search API integration

---

### 8. **actions/notes.py** - Note Taking
```
PURPOSE: Persist user notes to file
IMPORTS: built-ins only
KEY FUNCTION: save_note(content)
```

**save_note() logic:**
1. Open notes.txt in append mode
2. Write content + newline
3. Return "Note saved."

**File location:** notes.txt in project root

---

### 9. **ui/console.py** - Display
```
PURPOSE: Print formatted AI responses
IMPORTS: none
KEY FUNCTION: show(text)
```

**show() logic:**
- Input: text string
- Output: Prints `\nLUMO: {text}\n`
- Simple formatter for console display

---

### 10. **run.py** - Main Orchestration Loop
```
PURPOSE: Brings everything together in infinite loop
IMPORTS: All modules above
```

**Main Loop Logic:**
```
1. Initialize empty messages list
2. Define FUNCTIONS schema (for function calling)
3. Print "LUMO online. Speak."
4. LOOP:
   a. Wait for listen() → get user_text
   b. Append {role: "user", content: user_text}
   c. Call ask_llm(messages, FUNCTIONS)
   d. Check if reply has function_call:
      - YES: execute_action()
            show() result
            speak() result
            append {role: "function", content: result}
      - NO: show() text
            speak() text
            append {role: "assistant", content: text}
   e. Loop continues
```

**Message history:** Accumulated in `messages[]` throughout session

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ RUN.PY - Main Loop                                          │
└─────────────────────────────────────────────────────────────┘
                         ↓
          ┌──────────────────────────────┐
          │ 1. audio.stt.listen()        │
          │    ↓                         │
          │    Whisper API              │
          │    ↓                         │
          │    "hello world"            │
          └──────────────────────────────┘
                         ↓
          ┌──────────────────────────────┐
          │ 2. messages.append(           │
          │      role: "user",           │
          │      content: "hello world"  │
          │    )                         │
          └──────────────────────────────┘
                         ↓
          ┌──────────────────────────────────────────┐
          │ 3. core.llm.ask_llm(messages, FUNCTIONS)│
          │    ↓                                     │
          │    OpenAI GPT-4o                       │
          │    ↓                                     │
          │    Returns: {                           │
          │      "content": "...",                  │
          │      "function_call": {                 │
          │        "name": "web_search",           │
          │        "arguments": "{...}"            │
          │      }                                  │
          │    }                                    │
          └──────────────────────────────────────────┘
                         ↓
          ┌──────────────────────────────────────┐
          │ 4a. Function Call?                   │
          │     YES:                             │
          │     ↓                                │
          │     core.planner.execute_action()   │
          │     ↓                                │
          │     action/web_search.py or notes.py│
          │     ↓                                │
          │     Result                          │
          │     ↓                                │
          │     ui.console.show()               │
          │     audio.tts.speak()               │
          │                                      │
          │     NO:                             │
          │     ↓                                │
          │     ui.console.show(text)           │
          │     audio.tts.speak(text)           │
          │     messages.append({role: "assistant"})
          └──────────────────────────────────────┘
                         ↓
                    LOOP BACK
```

---

## Key Design Points

### 1. **Function Calling Protocol**
- LLM returns `function_call` with JSON string arguments
- `planner.py` parses JSON string to dict
- `execute_action()` dispatches to correct function
- Result appended back to messages as `role: "function"`

### 2. **Message History**
- All messages stored in `messages[]`
- Includes system context implicitly (in SYSTEM_PROMPT)
- Grows with each conversation turn
- Allows LLM to maintain context

### 3. **Error Handling**
- STT: Returns "" on error
- TTS: Returns False, prints warning
- Planner: Returns "Action not implemented"
- All try/except blocks in place

### 4. **API Dependencies**
- OpenAI: GPT-4o (mandatory for core)
- Whisper: Built into OpenAI
- ElevenLabs: Optional (graceful degradation)
- FAISS: Ready but not used yet

---

## What's Working ✓

✅ Config loading
✅ LLM initialization
✅ Function calling schema
✅ Memory class (add, search)
✅ Action routing
✅ Console output
✅ Web search stub
✅ Note saving
✅ Audio recording setup
✅ TTS error handling

---

## What Happens When You Run It

```
$ python run.py

LUMO online. Speak.
Listening...
[waits for audio input - must speak into microphone]
[sends to Whisper]
User's text transcribed
[sent to GPT-4o]
GPT-4o responds or calls function
[result shown and spoken]
Loop continues...
```

**Will block on listen()** - Waiting for you to speak

---

## Testing Notes

✓ All imports work
✓ All functions callable
✓ No syntax errors
✓ No missing dependencies
✓ Config loaded correctly
✓ Ready for live testing with microphone + API keys
