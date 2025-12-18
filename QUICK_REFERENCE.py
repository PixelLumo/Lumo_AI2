#!/usr/bin/env python3
"""Quick reference for LUMO learning and improvement system."""

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                 LUMO LEARNING & IMPROVEMENT SYSTEM                         ║
╚════════════════════════════════════════════════════════════════════════════╝

📚 DOCUMENTATION:
   • LEARNING.md          - Logging architecture (what, where, how)
   • IMPROVEMENT_LOOP.md  - Complete improvement cycle guide
   • learning/logger.py   - Core logging module (append-only JSONL)
   • learning/analyzer.py - Pattern detection from logs
   • learning/tuner.py    - Threshold adjustment suggestions
   • learning/feedback.py - Real-time feedback integration

🚀 QUICK START:

   1. Run LUMO normally for 20-50 interactions:
      $ python run.py
      (Just use it - logging happens automatically)

   2. Analyze collected data:
      $ python improvement_loop.py
      (Displays failure patterns and suggestions)

   3. Review suggestions and manually adjust thresholds:
      $ edit learning/tuning.json
      (Make tweaks based on analysis)

   4. Test adjusted system:
      $ python run.py
      (Another 20-50 interactions with new settings)

   5. Measure improvement:
      $ python improvement_loop.py
      (Compare metrics to previous baseline)

   6. Repeat steps 3-5 as needed!

📊 KEY METRICS:

   Success Rate          - % of interactions that succeeded
   Wake Word Detection   - % of times "lumo" was detected
   Failure Patterns      - Which intents fail most often
   Confirmation Rate     - How often users confirm destructive actions

⚙️  PARAMETERS YOU CAN TUNE:

   learning/tuning.json:
   • vad.silence_threshold      (0.001 - 0.1)   → Speech detection sensitivity
   • kws.pattern_threshold      (0.1 - 0.9)     → Wake word sensitivity
   • confirmation.timeout       (5 - 30 sec)    → Confirmation wait time

🔄 THE LOOP:

   Observe (read logs)
      ↓
   Log Outcomes (JSONL format - automatic)
      ↓
   Detect Patterns (analyze failures, success rates)
      ↓
   Adjust Thresholds (get suggestions, review, apply)
      ↓
   Re-test in Live Use (collect new data)
      ↓
   [Loop back to Observe]

🎯 GOALS:

   ✓ 95%+ success rate on queries
   ✓ 90%+ wake word detection
   ✓ 0% accidental actions (confirmation prevents this)
   ✓ Fast response times
   ✓ No false wake-ups

💡 TIPS:

   • Collect 50+ interactions before first tuning
   • Make small adjustments (0.01 changes at a time)
   • Test one parameter at a time
   • Give system 20-30 interactions to see impact
   • Use improvement_loop.py frequently for feedback
   • Never automatically apply changes - always review!

🔗 INTEGRATION:

   Learning happens automatically in run.py:

   from learning.logger import log_interaction

   log_interaction(
       wake_detected=True,
       transcript="user said this",
       intent="query",
       outcome="success"
   )

📁 FILE STRUCTURE:

   learning/
   ├── __init__.py           - Module exports
   ├── logger.py             - Core logging (append-only JSONL)
   ├── analyzer.py           - Pattern detection
   ├── tuner.py              - Threshold suggestions
   ├── feedback.py           - Real-time feedback
   ├── log.jsonl             - Interaction log (auto-created)
   └── tuning.json           - Threshold config (auto-created)

   improvement_loop.py       - Main analysis script (run this!)
   LEARNING.md              - Full logging docs
   IMPROVEMENT_LOOP.md      - Full improvement cycle docs

🚨 TROUBLESHOOTING:

   Q: Script fails with "No logs found"
   A: Run LUMO first with: python run.py
      Let it collect ~20 interactions before analyzing

   Q: Thresholds don't seem to change behavior
   A: Thresholds in tuning.json are suggestions only!
      Code must LOAD tuning.json to use new values (future)
      For now, adjust directly in: audio/vad.py, audio/kws.py

   Q: How to reset everything?
   A: Safe to delete:
      rm learning/log.jsonl
      rm learning/tuning.json
      Directories stay, fresh data will accumulate

📞 SUPPORT:

   All modules are self-documenting:
   python -c "from learning import analyzer; help(analyzer.analyze_failures)"

════════════════════════════════════════════════════════════════════════════════
""")
