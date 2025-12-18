# 30–60 Minute Live Session Guide

## Pre-Session Checklist

- [ ] `.env` file has `OPENAI_API_KEY` and `ELEVENLABS_API_KEY`
- [ ] Microphone is connected and working
- [ ] No background noise (or expect to see it in logs)
- [ ] Terminal ready to see real-time logging

## Start Session

```powershell
cd C:\Lumo_AI
& .venv/Scripts/Activate.ps1
python run.py
```

You will see:
```
LUMO online. Say 'LUMO' to activate.
🎤 Listening... (speak within 30 seconds)
```

## What You'll See In Real Time

### Turn Structure (Every Interaction)
Each turn prints:
```
[RAW_TRANSCRIPT] Turn 1: Length=25, Duration=2.34s, Content='lumo what is python'
[QUERY] 'what is python'
[MESSAGE_HISTORY] 0 messages before LLM call
[LLM_CALL] 1 messages, 2 functions available
[LLM_RESPONSE] Type: TEXT, Length: 145 chars
[TEXT_RESPONSE] 145 chars
```

### Function Call Turn
```
[RAW_TRANSCRIPT] Turn 2: Length=18, Duration=1.89s, Content='lumo search python'
[QUERY] 'search python'
[LLM_RESPONSE] Type: FUNCTION_CALL, Name: web_search
[LLM_ARGS] {"query": "python"}
[ACTION_RESULT] web_search -> Success
```

### Confirmation Turn
```
[RAW_TRANSCRIPT] Turn 3: Length=32, Duration=2.12s, Content='lumo save my notes for later'
[LLM_RESPONSE] Type: FUNCTION_CALL, Name: save_note
[CONFIRMATION_NEEDED] save_note
LUMO: Save note with content: 'my notes for later'. Say 'yes' to confirm.

[PENDING_CONFIRMATION] Waiting for: save_note
[RAW_TRANSCRIPT] Turn 4: Length=3, Duration=0.45s, Content='yes'
✓ Confirmed
[ACTION_RESULT] save_note -> Success
```

## Tag Failures As You Go

As you talk to the system, note any issues:

### UX Issues (Blocking)
- Silence detection fails (waits forever, times out too fast)
- Wake word too strict/loose
- Confirmation loop confusing
- Can't understand user speech

**Example log:**
```
[WAKE_WORD_SKIP] No 'lumo' detected in 'hello music please'  <- UX: too strict
```

### Logic Issues (Wrong Intent)
- LLM picks wrong function
- LLM misunderstands the command
- Query cleaning removes important words

**Example log:**
```
[QUERY] ''  <- Logic: "lumo save notes" becomes empty after wake word removal
[LLM_RESPONSE] Type: TEXT, Length: 0 chars  <- Logic: LLM has nothing to respond to
```

### Model Issues (Hallucination)
- LLM over-talks (rambles)
- LLM invents actions
- LLM ignores confirmation needed

**Example log:**
```
[LLM_RESPONSE] Type: TEXT, Length: 2847 chars  <- Model: suspiciously long
[LLM_ARGS] {"query": "how to make explosives"}  <- Model: hallucinated dangerous function
```

### System Issues (Crash)
- Audio fails
- API timeout
- Memory leak
- Crash without recovery

**Example log:**
```
[EXCEPTION] APIError: rate_limit_exceeded
[TRACEBACK] ...
[RECOVERY_PATH] State reset, continuing
```

## Files To Watch

### Real-Time Monitoring
- **Console output** — See `[RAW_TRANSCRIPT]`, `[LLM_RESPONSE]`, etc. as it happens
- **lumo.log** — Text-based audit trail, check after session

### Post-Session Analysis
- **session_data.jsonl** — One JSON object per line, machine-readable

```bash
# View all turns that had exceptions
Select-String '"exception"' session_data.jsonl

# View all LLM function calls
Select-String '"function_call"' session_data.jsonl

# View transcripts that failed wake word
Select-String '"wake_word_detected": false' session_data.jsonl

# Count turns by type
(Get-Content session_data.jsonl | ConvertFrom-Json | Group-Object -Property function_call).Count
```

## Sample Session (What Success Looks Like)

### Turn 1: Simple Question
```
[RAW_TRANSCRIPT] Turn 1: Length=20, Duration=1.45s, Content='lumo what time is it'
[QUERY] 'what time is it'
[MESSAGE_HISTORY] 0 messages before LLM call
[LLM_CALL] 1 messages, 2 functions available
[LLM_RESPONSE] Type: TEXT, Length: 35 chars
[TEXT_RESPONSE] 35 chars
LUMO: It is currently 3:45 PM on December 17, 2025.
```
✅ Clean flow, LLM responds with text

### Turn 2: Search Request
```
[RAW_TRANSCRIPT] Turn 2: Length=25, Duration=2.12s, Content='lumo search for machine learning'
[QUERY] 'search for machine learning'
[MESSAGE_HISTORY] 2 messages before LLM call
[LLM_CALL] 3 messages, 2 functions available
[LLM_RESPONSE] Type: FUNCTION_CALL, Name: web_search
[LLM_ARGS] {"query": "machine learning"}
[ACTION_EXECUTE] Calling web_search with args
[ACTION_RESULT] web_search -> Success
LUMO: I would search the web for: machine learning
```
✅ LLM correctly chose function_call

### Turn 3: Destructive Action + Confirmation
```
[RAW_TRANSCRIPT] Turn 3: Length=27, Duration=1.89s, Content='lumo save my learning notes'
[QUERY] 'save my learning notes'
[LLM_RESPONSE] Type: FUNCTION_CALL, Name: save_note
[LLM_ARGS] {"content": "my learning notes"}
[CONFIRMATION_NEEDED] save_note
LUMO: Save note with content: 'my learning notes'. Say 'yes' to confirm.

[PENDING_CONFIRMATION] Waiting for: save_note
[RAW_TRANSCRIPT] Turn 4: Length=3, Duration=0.30s, Content='yes'
[cleaned_transcript] 'yes'
✓ Confirmed
[ACTION_RESULT] save_note -> Success
LUMO: Note saved.
```
✅ Confirmation flow works

## Early Exit Points (When To Stop)

Stop if you see:
1. **Infinite loops** — System repeats same prompt
2. **API errors** — `APIError`, `rate_limit_exceeded` that don't recover
3. **Corrupted state** — Confirmation never clears, messages pile up unbounded
4. **Audio failure** — Can't hear anything for 5+ consecutive turns

Otherwise: **Keep going 30–60 minutes.** Let the failures emerge naturally.

## After Session: Analysis

1. Stop with `Ctrl+C`
2. Check `session_data.jsonl` for patterns
3. Review `lumo.log` for context around issues
4. Report to me with:
   - Count of successful turns
   - List of failures tagged as [UX], [Logic], [Model], [System]
   - Copy of session_data.jsonl

Example failure report:
```
Session: 45 minutes
Turns: 23 total
Successes: 19
Failures: 4

[UX] Turns 3,7,15: Wake word too strict, misses "hello lumo"
[Logic] Turn 12: Query becomes empty after "lumo save note" → "save note"  
[System] Turn 23: OpenAI timeout, recovered gracefully
```

---

**Goal:** Find real behavioral failures, not theoretical ones. Keep the system alive, watch it work (and fail), then fix grounded in evidence.
