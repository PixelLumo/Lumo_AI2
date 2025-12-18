import numpy as np
import time
from audio.kws import detect_keyword


def collect_utterance(audio_queue, vad_fn, timeout=2.0):
    """
    Collect speech after wake word detected.
    Uses VAD to trim silence, returns audio ready for STT.
    """
    frames = []
    last_speech = time.time()

    while True:
        try:
            chunk = audio_queue.get(timeout=0.1)
        except TimeoutError:
            if time.time() - last_speech > timeout:
                break
            continue

        if vad_fn(chunk):
            last_speech = time.time()
            frames.append(chunk)

    if not frames:
        return None

    return np.concatenate(frames, axis=0)


def wait_for_wake_word(audio_queue, wake_keyword="lumo", timeout=60):
    """
    Listen for wake word using KWS (no Whisper overhead).

    Args:
        audio_queue: Queue of audio chunks
        wake_keyword: Keyword to detect (default "lumo")
        timeout: Seconds to listen before giving up

    Returns:
        bool: True if wake word detected
    """
    start_time = time.time()
    frame_count = 0

    print(f"🎤 Listening for '{wake_keyword}'...")

    while time.time() - start_time < timeout:
        try:
            chunk = audio_queue.get(timeout=0.5)
            frame_count += 1

            # Lightweight KWS check (no Whisper)
            if detect_keyword(chunk):
                print(f"✓ Wake word detected! ({frame_count} frames analyzed)")
                return True

            # Progress indicator
            if frame_count % 50 == 0:
                print(f"  ... {frame_count} frames processed")

        except TimeoutError:
            continue

    print(f"⏱ Timeout: No wake word detected after {timeout}s")
    return False
