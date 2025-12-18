import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
from faster_whisper import WhisperModel
import webrtcvad

# Initialize models
whisper_model = WhisperModel("base", compute_type="int8")
vad = webrtcvad.Vad(2)  # Aggressiveness: 0=least aggressive, 3=most aggressive

SAMPLE_RATE = 16000
FRAME_DURATION_MS = 20  # VAD uses 10, 20, or 30ms frames
SILENCE_FRAMES = 15  # ~300ms of silence triggers end of speech

def transcribe(audio_array):
    """
    Transcribe audio numpy array using Faster-Whisper.

    Args:
        audio_array: numpy array of audio samples (16kHz, mono, float32)

    Returns:
        str: Transcribed text
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, SAMPLE_RATE, audio_array.astype(np.float32))
        segments, _ = whisper_model.transcribe(f.name)

    text = " ".join(seg.text for seg in segments).strip()
    return text

def _is_speech(audio_chunk):
    """
    Detect if audio chunk contains speech using WebRTC VAD.

    Args:
        audio_chunk: numpy array of audio samples

    Returns:
        bool: True if speech detected
    """
    # Convert float32 to int16 for VAD
    audio_int16 = (audio_chunk * 32767).astype(np.int16)
    try:
        return vad.is_speech(audio_int16.tobytes(), SAMPLE_RATE)
    except Exception:
        return False

def listen_continuous(timeout=30, wake_word="lumo"):
    """
    Continuous listening with VAD (Voice Activity Detection).

    Architecture:
    Mic Stream → VAD (noise gate) → Wake Word Check → Speech Buffer → STT

    Args:
        timeout: Max seconds to listen for wake word (default 30)
        wake_word: Wake word to detect (default "lumo")

    Returns:
        tuple: (transcribed_text, audio_duration_seconds)
    """
    chunk_size = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

    print("🎤 Listening for wake word...")
    audio_buffer = []
    silence_counter = 0
    wake_word_detected = False

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            blocksize=chunk_size
        ) as stream:
            while True:
                # Read audio chunk
                audio_chunk, _ = stream.read(chunk_size)
                audio_chunk = audio_chunk.flatten()

                # VAD: Detect if this chunk contains speech
                has_speech = _is_speech(audio_chunk)

                if has_speech:
                    silence_counter = 0
                    if not wake_word_detected:
                        # Check for wake word in this chunk
                        with tempfile.NamedTemporaryFile(
                            suffix=".wav", delete=False
                        ) as f:
                            wav.write(
                                f.name,
                                SAMPLE_RATE,
                                audio_chunk.astype(np.float32)
                            )
                            segments, _ = whisper_model.transcribe(f.name)
                            chunk_text = (
                                " ".join(
                                    seg.text for seg in segments
                                ).strip().lower()
                            )

                        if wake_word in chunk_text:
                            print(f"✓ Wake word '{wake_word}' detected!")
                            wake_word_detected = True
                            audio_buffer = []  # Reset buffer after wake word
                            silence_counter = 0
                    else:
                        # After wake word, buffer speech
                        audio_buffer.extend(audio_chunk)
                else:
                    # Silence detected
                    if wake_word_detected:
                        silence_counter += 1
                        # Include silence in buffer
                        audio_buffer.extend(audio_chunk)
                        # End speech on sustained silence
                        if silence_counter >= SILENCE_FRAMES:
                            print("🔇 Speech ended (silence detected)")
                            break
                    # If wake word not detected yet, keep listening

                # Timeout if no wake word detected
                if (
                    not wake_word_detected
                    and len(audio_buffer) / SAMPLE_RATE > timeout
                ):
                    print("⏱ Timeout: No wake word detected")
                    return "", 0

    except KeyboardInterrupt:
        print("⏹ Listening stopped")
        return "", 0

    # Transcribe buffered speech
    if audio_buffer:
        audio_array = np.array(audio_buffer, dtype=np.float32)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            wav.write(f.name, SAMPLE_RATE, audio_array)
            segments, _ = whisper_model.transcribe(f.name)

        text = " ".join(seg.text for seg in segments).strip()
        duration = len(audio_buffer) / SAMPLE_RATE
        return text, duration

    return "", 0

def listen(seconds=5):
    """
    Legacy fixed-duration listening (for testing).

    Args:
        seconds: Duration to listen

    Returns:
        tuple: (transcribed_text, audio_duration)
    """
    fs = 16000
    audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, fs, audio.astype(np.float32))
        segments, _ = whisper_model.transcribe(f.name)

    text = " ".join(seg.text for seg in segments).strip()
    return text, seconds
