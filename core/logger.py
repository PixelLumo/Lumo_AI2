"""
LUMO Logging Module
Tracks transcripts, decisions, function calls, and errors for debugging
"""

import json
import os
from datetime import datetime

class Logger:
    def __init__(
        self,
        log_file="lumo.log",
        session_file="session_data.jsonl"
    ):
        self.log_file = log_file
        self.session_file = session_file  # Structured turn-by-turn data
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._init_log()

    def _init_log(self):
        """Create log file with session header"""
        with open(self.log_file, "a") as f:
            f.write("\n" + "="*80 + "\n")
            f.write(f"SESSION START: {datetime.now().isoformat()}\n")
            f.write("="*80 + "\n")

    def _write(self, category, data):
        """Write log entry with timestamp and category"""
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] [{category}] {data}\n"

        with open(self.log_file, "a") as f:
            f.write(entry)

    def transcribed(self, text, duration=None):
        """Log speech transcription"""
        msg = f"STT: '{text}'"
        if duration:
            msg += f" ({duration:.2f}s)"
        self._write("TRANSCRIBE", msg)

    def wake_word_check(self, text, detected):
        """Log wake word detection result"""
        status = "[DETECTED]" if detected else "[NOT_DETECTED]"
        self._write("WAKE_WORD", f"{status}: '{text}'")

    def llm_call(self, messages_count, functions_count):
        """Log LLM call"""
        self._write(
            "LLM_CALL",
            f"Messages: {messages_count}, Functions: {functions_count}"
        )

    def llm_response(self, response_type, content):
        """Log LLM response"""
        if response_type == "text":
            self._write("LLM_RESPONSE", f"TEXT: {content[:100]}...")
        elif response_type == "function":
            self._write("LLM_RESPONSE", f"FUNCTION_CALL: {content}")

    def action_executed(self, action_name, arguments, result):
        """Log action execution"""
        self._write(
            "ACTION",
            f"{action_name}({arguments}) -> {result[:100]}"
        )

    def action_pending_confirmation(self, action_name, arguments):
        """Log when action waits for confirmation"""
        self._write("CONFIRMATION", f"PENDING: {action_name}({arguments})")

    def action_confirmed(self, action_name, confirmed):
        """Log confirmation decision"""
        status = "[CONFIRMED]" if confirmed else "[REJECTED]"
        self._write("CONFIRMATION", f"{status}: {action_name}")

    def tts_executed(self, text):
        """Log text-to-speech execution"""
        self._write("TTS", f"Speak: '{text[:100]}...'")

    def error(self, error_type, message):
        """Log errors"""
        self._write("ERROR", f"{error_type}: {message}")

    def info(self, message):
        """Log info messages"""
        self._write("INFO", message)

    def log_turn(self, turn_data):
        """
        Log a complete turn with all reconstruction fields.
        Appends to session_data.jsonl for later analysis.

        turn_data dict should contain:
            - timestamp
            - raw_audio_duration
            - raw_transcript
            - cleaned_transcript
            - wake_word_detected
            - llm_input_context_size
            - llm_raw_response
            - function_call (optional)
            - final_output
            - exception (optional)
            - recovery_path (optional)
        """
        try:
            with open(self.session_file, "a") as f:
                f.write(json.dumps(turn_data, default=str) + "\n")
        except Exception as e:
            self._write("ERROR", f"Failed to log turn: {e}")

    def get_session_log(self):
        """Read current session log"""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                return f.read()
        return ""

# Global logger instance
logger = Logger()
