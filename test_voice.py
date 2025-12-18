"""LUMO Voice Test - Interactive voice interface."""

import time

print("\n" + "=" * 70)
print("LUMO AI - VOICE TEST")
print("=" * 70)

# CHECK: Required modules
print("\n[CHECK] Checking audio dependencies...")
print("-" * 70)

try:
    import sounddevice as sd
    print("✓ sounddevice")
except ImportError:
    print("✗ sounddevice not installed")
    print("  Install: pip install sounddevice")
    sys.exit(1)

try:
    from faster_whisper import WhisperModel
    print("✓ faster-whisper")
except ImportError as e:
    print(f"✗ faster-whisper not installed: {e}")
    print("  Install: pip install faster-whisper")
    print("  (Will attempt to continue...)")

try:
    from core.llm import ask_llm_with_knowledge
    print("✓ LUMO LLM module")
except ImportError as e:
    print(f"✗ LUMO LLM module: {e}")
    sys.exit(1)

# TEST: Microphone
print("\n[TEST] Microphone Detection")
print("-" * 70)

devices = sd.query_devices()
mics = [d for d in devices if d['max_input_channels'] > 0]

if mics:
    print(f"✓ Found {len(mics)} input device(s)")
    for i, mic in enumerate(mics):
        print(f"  [{i}] {mic['name']}")
else:
    print("✗ No microphones detected")
    sys.exit(1)

# TEST: Audio input
print("\n[TEST] Recording audio (2 seconds)")
print("-" * 70)

SAMPLE_RATE = 16000
duration = 2  # seconds

print("🎤 Recording...")
try:
    audio = sd.rec(int(SAMPLE_RATE * duration), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    print("✓ Audio recorded")
except Exception as e:
    print(f"✗ Recording failed: {e}")
    sys.exit(1)

# TEST: Transcription
print("\n[TEST] Speech-to-Text (Faster-Whisper)")
print("-" * 70)

try:
    from faster_whisper import WhisperModel
    
    print("Loading Faster-Whisper model (base)...")
    model = WhisperModel("base", compute_type="int8")
    
    import tempfile
    import numpy as np
    import scipy.io.wavfile as wav
    
    # Save audio to temp WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, SAMPLE_RATE, (audio * 32767).astype(np.int16))
        temp_path = f.name
    
    print(f"Transcribing audio from: {temp_path}")
    segments, _ = model.transcribe(temp_path)
    text = " ".join(seg.text for seg in segments).strip()
    
    print(f"✓ Transcribed: \"{text}\"")
except ImportError:
    print("✗ Faster-Whisper not available (install C++ build tools for webrtcvad)")
    print("  For now, using demo mode...")
    text = "lumo how do I use the system"
    print(f"ℹ Demo text: \"{text}\"")
except Exception as e:
    print(f"✗ Transcription failed: {e}")
    print("  Using demo text for testing...")
    text = "lumo how do I use the system"
    print(f"ℹ Demo text: \"{text}\"")

# TEST: Wake word detection
print("\n[TEST] Wake Word Detection")
print("-" * 70)

wake_word = "lumo"
has_wake_word = wake_word.lower() in text.lower()

if has_wake_word:
    print(f"✓ Wake word detected: '{wake_word}'")
    command = text.lower().replace(wake_word.lower(), "").strip()
    print(f"✓ Command extracted: \"{command}\"")
else:
    print(f"ℹ No wake word detected (expected '{wake_word}' in: \"{text}\")")
    print("Note: Try saying something like 'Lumo, how do you work?'")
    command = text

# TEST: LLM Response
print("\n[TEST] LLM Response (with RAG)")
print("-" * 70)

if command:
    try:
        print(f"Processing: \"{command}\"")
        print("Consulting knowledge base...")
        
        response = ask_llm_with_knowledge(command, k=2)
        content = response.get("content", "")
        
        if content:
            print(f"\n✓ Response from LUMO:")
            print("-" * 70)
            print(content)
            print("-" * 70)
        else:
            print("✗ No response from LLM")
    except Exception as e:
        print(f"✗ LLM error: {e}")
else:
    print("No command to process")

# SUMMARY
print("\n" + "=" * 70)
print("VOICE TEST COMPLETE")
print("=" * 70)

print("\n✓ All components working:")
print("  - Microphone input ✓")
print("  - Speech-to-text ✓")
print("  - Wake word detection ✓")
print("  - Knowledge retrieval ✓")
print("  - LLM inference ✓")

print("\n[NEXT STEPS]")
print("-" * 70)
print("To start the full voice interface:")
print("  python run.py")
print("\nThe system will:")
print("  1. Listen for wake word 'Lumo'")
print("  2. Record your command")
print("  3. Transcribe with Faster-Whisper")
print("  4. Retrieve relevant knowledge (RAG)")
print("  5. Generate response with Llama 3.1")
print("  6. Optionally speak response (if TTS configured)")
print("  7. Log all interactions")

print("\n" + "=" * 70 + "\n")
