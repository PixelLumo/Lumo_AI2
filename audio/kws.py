"""
Keyword Spotting (KWS) - Lightweight wake word detection
Runs continuously without Whisper overhead
"""

import numpy as np
from collections import deque

SAMPLE_RATE = 16000
MFCC_COEFF = 13

# Simple pattern: RMS energy spike detection for "lumo"
# In production, this would use a lightweight neural net (TFLite, ONNX)
# For now: energy-based detection with configurable threshold


class KeywordSpotter:
    def __init__(self, keyword="lumo", threshold=0.3):
        self.keyword = keyword
        self.threshold = threshold
        self.history = deque(maxlen=32)  # 2 seconds of frames at 16 frames/sec
        self.last_spike = 0

    def detect(self, audio_chunk):
        """
        Detect keyword in audio chunk.

        Args:
            audio_chunk: numpy array of audio samples

        Returns:
            bool: True if keyword likely present
        """
        # Extract simple features: RMS energy
        rms = np.sqrt(np.mean(audio_chunk ** 2))
        self.history.append(rms)

        # Look for characteristic pattern of "lumo" (short, two syllables)
        if len(self.history) < 8:
            return False

        recent = list(self.history)[-8:]

        # Pattern: Two peaks separated by dip
        # "lu" peak, "mo" peak
        has_peak1 = any(e > self.threshold for e in recent[:4])
        has_peak2 = any(e > self.threshold for e in recent[4:])

        if has_peak1 and has_peak2:
            return True

        return False


# Singleton instance
_kws = None


def init_kws(keyword="lumo", threshold=0.3):
    """Initialize keyword spotter."""
    global _kws
    _kws = KeywordSpotter(keyword=keyword, threshold=threshold)


def detect_keyword(audio_chunk):
    """
    Check if keyword is present in audio chunk.
    Lightweight alternative to Whisper for wake word detection.

    Args:
        audio_chunk: numpy array of audio samples

    Returns:
        bool: True if keyword detected
    """
    global _kws
    if _kws is None:
        init_kws()

    return _kws.detect(audio_chunk)
