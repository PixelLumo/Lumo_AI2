# LUMO Learning Architecture

## Overview

LUMO now tracks all interactions in an append-only learning log. This enables:

1. **Performance Analysis** - What works, what fails
2. **User Behavior Understanding** - Most common commands
3. **Policy Learning** - Foundation for future self-improvement
4. **Debugging** - Complete audit trail of decisions

## Architecture

```
Audio Input
    ↓ [VAD Detection]
Wake Word Detected?
    ↓
Intent Recognition
    ↓
Action Execution
    ↓
Outcome Tracking
    ↓
Learning Log (JSONL)
    ↓
Policy Adjustment (future)
```

## Learning Log Format

**File:** `learning/log.jsonl`

Each interaction is one JSON line:

```json
{
  "timestamp": "2025-12-17T21:10:00",
  "wake_detected": true,
  "transcript": "lumo turn off the lights",
  "intent": "device_control",
  "action": "lights_off",
  "confirmed": false,
  "outcome": "success",
  "error": null
}
```

### Fields

| Field | Type | Meaning |
|-------|------|---------|
| `timestamp` | ISO8601 | When the interaction occurred |
| `wake_detected` | bool | Did we detect the wake word? |
| `transcript` | str | What the user said (STT output) |
| `intent` | str | Detected intent (query, device_control, etc.) |
| `action` | str | What action was taken |
| `confirmed` | bool/null | User confirmation for destructive actions |
| `outcome` | str | success, failed, cancelled, pending |
| `error` | str/null | Error message if failed |

## Usage

### View Learning Statistics

```bash
python scripts/inspect_learning_log.py
```

Shows:
- Total interactions count
- Wake word detection rate
- Success/failure breakdown
- Log file location and size

### Test the Learning System

```bash
python test_learning_log.py
```

Creates sample interactions and verifies logging works.

### Access Logs Programmatically

```python
from learning.logger import log_interaction, get_recent_logs, get_stats

# Log an interaction
log_interaction(
    wake_detected=True,
    transcript="lumo what time is it",
    intent="query",
    outcome="success"
)

# Retrieve recent logs
logs = get_recent_logs(n=10)  # Last 10 interactions

# Get statistics
stats = get_stats()
print(f"Success rate: {stats['success_rate']:.1f}%")
```

## Data Flow in run.py

### Phase 1: Wake Word Detection
- **Logged:** `wake_detected=True/False`
- **Intent:** None (waiting)

### Phase 2: Speech Collection
- **Logged:** `transcript=""` if no speech
- **Outcome:** "failed" if timeout

### Phase 3: Transcription
- **Logged:** `transcript="user command"`
- **Logged:** Full text from STT

### Phase 4: Destructive Check
- **Logged:** `intent="destructive_action"`
- **Logged:** `confirmed=None` (awaiting response)

### Phase 5: Confirmation Response
- **Logged:** `confirmed=True/False`
- **Logged:** `intent="confirmation"`

### Phase 6: LLM Response
- **Logged:** `intent="query"`
- **Logged:** `outcome="success"`

## Policy Learning (Future)

Once logs accumulate, we can:

1. **Identify Common Failures**
   - Which commands fail most?
   - Which intents are misclassified?

2. **Optimize Parameters**
   - VAD threshold adjustments
   - KWS sensitivity tuning

3. **Learn User Preferences**
   - Most common request types
   - Time-of-day patterns

4. **Safety Improvements**
   - Detect dangerous patterns
   - Improve confirmation logic

## Example Log Analysis

```python
from learning.logger import get_recent_logs

logs = get_recent_logs(100)

# Find all successful device control commands
device_commands = [
    log for log in logs 
    if log['intent'] == 'device_control' 
    and log['outcome'] == 'success'
]

# Analyze most common actions
actions = [log['action'] for log in device_commands]
print(f"Most common: {max(set(actions), key=actions.count)}")

# Success rate for confirmations
confirmations = [log for log in logs if log['intent'] == 'confirmation']
success_count = sum(1 for log in confirmations if log['outcome'] == 'success')
rate = (success_count / len(confirmations)) * 100
print(f"Confirmation success: {rate:.1f}%")
```

## Privacy & Storage

- **Storage:** Local only (no cloud sync)
- **Format:** Plain JSON (human-readable)
- **Retention:** Indefinite (append-only)
- **Access:** Programmatic via logger module

All learning happens locally without external calls.

## Next Steps

1. ✅ Logging infrastructure (done)
2. ⏳ Statistics dashboard
3. ⏳ Automated parameter tuning
4. ⏳ Pattern detection for safety
5. ⏳ User behavior adaptation

