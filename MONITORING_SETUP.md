# STRUCTURED MONITORING READY

## Changes Made

### 1. **audio/stt.py** — Returns Tuple
- `listen()` now returns `(transcript, duration_seconds)` instead of just text
- Tracks total audio length for reconstruction
- Updated all return paths (timeout, success, error)

### 2. **core/logger.py** — Structured Session Logging
- New method: `log_turn(turn_data)` 
- Appends JSON to `session_data.jsonl` (one object per turn)
- All 10 reconstruction fields captured:
  ```
  turn, timestamp, raw_audio_duration, raw_transcript, 
  cleaned_transcript, wake_word_detected, llm_input_context_size,
  llm_raw_response, function_call, final_output, exception, recovery_path
  ```

### 3. **run.py** — Comprehensive Turn Logging
- Added `TURN_NUM` counter (1-based indexing)
- Creates `turn_data` dict at start of each loop
- Populates all 10 fields as turn progresses
- Calls `logger.log_turn(turn_data)` at end of turn
- Full exception handling with recovery path logging
- Unpacks tuple from `listen()`: `user_text, audio_duration = result`

### 4. **SESSION_GUIDE.md** — New
- Complete 30–60 minute session instructions
- How to tag failures (UX, Logic, Model, System)
- Real-time monitoring tips
- Post-session analysis commands
- Example success flows

## What Gets Logged

### Console (Real-Time)
```
[RAW_TRANSCRIPT] Turn 1: Length=20, Duration=1.45s, Content='lumo ...'
[QUERY] '...'
[MESSAGE_HISTORY] 0 messages before LLM call
[LLM_CALL] 1 messages, 2 functions available
[LLM_RESPONSE] Type: FUNCTION_CALL, Name: web_search
[LLM_ARGS] {"query": "python"}
[ACTION_RESULT] web_search -> Success
```

### lumo.log (Human-Readable)
```
================================================================================
SESSION START: 2025-12-17T23:17:03.123456
================================================================================
[2025-12-17T23:17:05.234567] [TRANSCRIBE] STT: 'lumo search python'
[2025-12-17T23:17:06.345678] [WAKE_WORD] [DETECTED]: 'lumo search python'
[2025-12-17T23:17:07.456789] [ACTION] web_search({'query': 'python'}) -> success
```

### session_data.jsonl (Machine-Readable)
```json
{"turn": 1, "timestamp": "2025-12-17T23:17:05.234567", "raw_audio_duration": 1.45, "raw_transcript": "lumo search python", "cleaned_transcript": "search python", "wake_word_detected": true, "llm_input_context_size": 1, "llm_raw_response": {"content": "", "function_call": {"name": "web_search", "arguments": "{\"query\": \"python\"}"}}, "function_call": {"name": "web_search", "arguments": "{\"query\": \"python\"}"}, "final_output": "I would search the web for: python", "exception": null, "recovery_path": null}
```

## Run Command

```powershell
cd C:\Lumo_AI
& .venv/Scripts/Activate.ps1
python run.py
```

## Quick Analysis After Session

```powershell
# See all exceptions
(Get-Content session_data.jsonl | ConvertFrom-Json | Where-Object {$_.exception}) | Format-Table turn, timestamp, exception

# Count function calls
(Get-Content session_data.jsonl | ConvertFrom-Json | Where-Object {$_.function_call}) | Measure-Object

# Check wake word performance
(Get-Content session_data.jsonl | ConvertFrom-Json | Group-Object wake_word_detected | Format-Table Name, Count)

# Find failed turns
(Get-Content session_data.jsonl | ConvertFrom-Json | Where-Object {$_.exception -or ($_.final_output -match "error")})
```

## Key Insight

You now have **two logs**:
- **lumo.log** — Real-time operational log (human debugging)
- **session_data.jsonl** — Structured session data (post-analysis, machine-readable)

Every turn is reconstructable. Every failure is tagged. Run for 30–60 minutes and let the system show you what actually breaks.
