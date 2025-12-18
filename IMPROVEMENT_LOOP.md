# LUMO Operational Improvement Loop

## Overview

LUMO implements a complete **data-driven improvement cycle**:

```
┌─────────────────────────────────────────────────────────┐
│  1. OBSERVE BEHAVIOR (from logs)                        │
├─────────────────────────────────────────────────────────┤
│  2. LOG OUTCOMES (JSONL format)                         │
├─────────────────────────────────────────────────────────┤
│  3. DETECT PATTERNS (failure analysis)                  │
├─────────────────────────────────────────────────────────┤
│  4. ADJUST THRESHOLDS/RULES (tuning suggestions)        │
├─────────────────────────────────────────────────────────┤
│  5. RE-TEST IN LIVE USE (measure improvement)           │
└─────────────────────────────────────────────────────────┘
```

This creates a **continuous feedback loop** that makes LUMO self-improving.

---

## Architecture

### 1. Pattern Detection (`learning/analyzer.py`)

Analyzes logs to identify:

- **Failure Patterns** - What fails and why
- **Success Rates** - Overall and per-intent
- **Wake Word Performance** - Detection accuracy
- **Confirmation Behavior** - User confirmation patterns
- **Improvement Opportunities** - Specific recommendations

```python
from learning.analyzer import (
    analyze_failures,
    analyze_success_rate,
    analyze_wake_word_detection,
    find_improvement_opportunities,
)

logs = get_recent_logs(100)
failures = analyze_failures(logs)
opportunities = find_improvement_opportunities(logs)
```

### 2. Threshold Tuning (`learning/tuner.py`)

Automatically suggests parameter adjustments:

- **VAD Silence Threshold** - Voice activity detection sensitivity
- **KWS Pattern Threshold** - Wake word detection sensitivity
- **Confirmation Timeout** - Time to wait for user response

```python
from learning.tuner import auto_tune, load_tuning_config, apply_adjustment

# Get suggestions
tuning = auto_tune(logs)
print(tuning["suggested_adjustments"])

# Load current config
config = load_tuning_config()
print(config["vad"]["silence_threshold"])

# Apply adjustment (manual review first!)
apply_adjustment("vad.silence_threshold", 0.008)
```

### 3. Real-time Feedback (`learning/feedback.py`)

Monitors system during operation:

- **Alerts** - High failure rates, low detection rates
- **Retest Scenarios** - What to test after adjustments
- **Status Display** - Current improvement status

```python
from learning.feedback import (
    check_improvement_needed,
    suggest_retest_scenario,
    print_improvement_status,
)

# Check if system needs improvement
logs = get_recent_logs(100)
needs = check_improvement_needed(logs)
if needs["improvement_needed"]:
    for alert in needs["alerts"]:
        print(f"⚠️  {alert['type']}: {alert['message']}")
        print(f"    Action: {alert['action']}")
```

---

## Running the Improvement Loop

### Complete Analysis (Recommended)

```bash
python improvement_loop.py
```

This runs all 5 steps and displays a complete improvement report:

```
================================================================================
  STEP 1: OBSERVE BEHAVIOR
================================================================================
✅ Observing 100 recent interactions

📊 Overall Statistics:
   Total Interactions: 100
   Success Rate: 82.0%
   Successful Actions: 82 / 100

================================================================================
  STEP 3: DETECT PATTERNS
================================================================================

❌ Failure Analysis:
   Total Failures: 18 (18.0%)
   By Type: {'failed': 12, 'cancelled': 6}
   Patterns Detected:
     • device_control: 15.0% failure rate
       Error: Action not found

✅ Success Analysis:
   Overall Rate: 82.0%
   By Intent:
     • query: 95.0% (19 / 20)
     • device_control: 75.0% (45 / 60)
     • confirmation: 100.0% (20 / 20)

================================================================================
  STEP 4: ADJUST THRESHOLDS / RULES
================================================================================

📋 Current Thresholds:
   vad_silence_threshold: 0.01
   kws_pattern_threshold: 0.3
   confirmation_timeout: 10

⚠  Suggested Adjustments (1):

   Parameter: kws.pattern_threshold
   Current: 0.3
   Suggested: 0.255
   Reason: Wake word fails in 12.5% of interactions...
```

### Individual Analyses

```python
from learning.analyzer import analyze_failures, analyze_success_rate

logs = get_recent_logs(100)

# Just failure analysis
failures = analyze_failures(logs)
print(f"Failure Rate: {failures['failure_rate']}")
print(f"Patterns: {failures['patterns']}")

# Just success analysis
success = analyze_success_rate(logs)
print(f"Overall: {success['overall_success_rate']}")
for intent, stats in success["by_intent"].items():
    print(f"  {intent}: {stats['rate']}")
```

### Manual Threshold Adjustment

```python
from learning.tuner import apply_adjustment, load_tuning_config, save_tuning_config

# 1. Load current config
config = load_tuning_config()

# 2. Review suggestions (from improvement_loop.py)
# 3. Manually adjust if you agree
config["kws"]["pattern_threshold"] = 0.25  # Lower = more sensitive

# 4. Save
save_tuning_config(config)

# 5. Test in live use
# 6. Run improvement_loop.py again to measure impact
```

---

## Data Flow

### Observation Phase

```
Logs (learning/log.jsonl)
    ↓
Retrieve last N (default 100)
    ↓
Analyze by intent, outcome, error
```

### Detection Phase

```
Patterns:
- High failure rates in specific intents
- Low wake word detection
- Unconfirmed user rejections
- Common error messages

Metrics:
- Overall success rate
- Per-intent success rates
- Wake word detection rate
- Confirmation rates
```

### Adjustment Phase

```
Current State → Analyze → Suggest → Review → Apply

Example:
- VAD detection: 82%
- Suggestion: Lower threshold to 0.008 (increase sensitivity)
- Impact: May increase false positives
- Manual Review: Approve? Decline?
```

### Re-test Phase

```
Collect 10-20 new interactions
    ↓
Run improvement_loop.py again
    ↓
Compare metrics before/after
    ↓
Iterate if needed
```

---

## Tuning Configuration

**File:** `learning/tuning.json`

```json
{
  "vad": {
    "silence_threshold": 0.01,
    "description": "RMS energy threshold for VAD",
    "min": 0.001,
    "max": 0.1,
    "tuned_at": "2025-12-18T12:00:00"
  },
  "kws": {
    "pattern_threshold": 0.3,
    "description": "RMS pattern matching threshold for wake word",
    "min": 0.1,
    "max": 0.9,
    "tuned_at": null
  },
  "confirmation": {
    "timeout_seconds": 10,
    "description": "Time to wait for user confirmation",
    "min": 5,
    "max": 30,
    "tuned_at": null
  }
}
```

---

## Interpretation Guide

### Success Rates

| Rate | Interpretation | Action |
|------|---|---|
| > 95% | Excellent | No changes needed |
| 85-95% | Good | Monitor, optimize on next review |
| 70-85% | Acceptable | Address largest failure categories |
| < 70% | Poor | Debug and adjust thresholds |

### Wake Word Detection

| Rate | Interpretation | Action |
|------|---|---|
| > 90% | Excellent | Keep current KWS threshold |
| 80-90% | Good | Monitor for patterns |
| 70-80% | Acceptable | Consider lowering threshold |
| < 70% | Poor | Significantly lower KWS threshold |

### Failure Patterns

| Pattern | Typical Cause | Typical Fix |
|---------|---|---|
| "Empty transcription" | Speech buffer timeout | Increase SILENCE_FRAMES |
| "Wake word detection failed" | KWS threshold too high | Lower pattern_threshold |
| "No speech detected" | VAD threshold too high | Lower silence_threshold |
| High cancellations | Confirmation requests too aggressive | Review DESTRUCTIVE_KEYWORDS |

---

## Example Workflow

### Day 1: Initial Setup
```bash
# Run LUMO, interact with it ~50 times
python run.py

# After 50 interactions, check baseline
python improvement_loop.py
# Output: Success rate 75%, main issues with device_control
```

### Day 2: Adjustment
```bash
# Review suggestions from analysis
# Increase KWS sensitivity (lower threshold 0.30 → 0.25)
# Edit learning/tuning.json manually

# Test adjusted system
python run.py
# ~30 more interactions focused on wake word
```

### Day 3: Re-test
```bash
# Measure improvement
python improvement_loop.py
# Output: Success rate 82% (improvement!), KWS now 95% accurate

# Continue testing other features
```

### Ongoing
```bash
# Run improvement_loop.py every 50-100 interactions
# Make small adjustments based on patterns
# Track metrics over time for trends
```

---

## Integration with run.py

The improvement loop is built on `run.py`'s logging infrastructure:

```python
# In run.py, every action is logged
log_interaction(
    wake_detected=True,
    transcript="user said this",
    intent="device_control",
    action="lights_off",
    confirmed=True,
    outcome="success"
)

# Improvement loop analyzes these logs
from learning.analyzer import find_improvement_opportunities
recs = find_improvement_opportunities()
```

No code changes needed — the logging happens automatically!

---

## Safety First

⚠️ **Important**: Adjustments are **suggested but never applied automatically**.

1. Analysis runs and suggests changes
2. You review the suggestions
3. You manually edit `learning/tuning.json`
4. System uses new thresholds on next run
5. You test and verify improvement
6. If bad, revert manually

This prevents accidental degradation!

---

## Future Enhancements

- 🔄 Automatic A/B testing (test new threshold on subset)
- 📊 Dashboard with historical trends
- 🤖 Machine learning for threshold prediction
- 🔔 Alerts when metrics cross thresholds
- 📁 Export analysis reports (CSV, JSON)
- 🌐 Cloud sync of anonymized metrics (optional)

