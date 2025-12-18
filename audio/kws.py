def detect_wake_word(audio_data: bytes) -> bool:
    """Dummy KWS - returns True for demo."""
    return True


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
