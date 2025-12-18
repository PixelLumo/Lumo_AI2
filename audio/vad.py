import numpy as np

SILENCE_THRESHOLD = 0.01


def is_speech(audio_chunk):
    rms = np.sqrt(np.mean(audio_chunk**2))
    return rms > SILENCE_THRESHOLD
