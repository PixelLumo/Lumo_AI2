# LUMO Voice Interface Guide

## Overview

LUMO now supports **voice interaction** with full RAG (Retrieval-Augmented Generation) capabilities. You can speak commands to LUMO and get intelligent, knowledge-grounded responses.

## Voice Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    VOICE INTERFACE                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  MICROPHONE INPUT                                       │
│       ↓                                                 │
│  AUDIO RECORDING (2-3 seconds)                          │
│       ↓                                                 │
│  VOICE ACTIVITY DETECTION (WebRTC VAD)                  │
│       ↓                                                 │
│  SPEECH-TO-TEXT (Faster-Whisper)                        │
│       ↓                                                 │
│  WAKE WORD DETECTION ("lumo")                           │
│       ↓                                                 │
│  COMMAND EXTRACTION                                     │
│       ↓                                                 │
│  SEMANTIC SEARCH (Knowledge Base RAG)                   │
│       ↓                                                 │
│  LLM INFERENCE (Ollama + Llama 3.1)                     │
│       ↓                                                 │
│  TEXT-TO-SPEECH (Optional)                              │
│       ↓                                                 │
│  AUDIO OUTPUT / LOGGING                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Start Ollama

First, ensure Ollama is running:

```bash
ollama serve
```

**Note**: You should see "Ollama is running on localhost:11434"

### 2. Test Voice Demo

Run the voice interface demo:

```bash
python test_voice_demo.py
```

**Output**:
- ✓ Microphone detection (lists available devices)
- ✓ Knowledge base search (RAG working)
- ✓ Wake word detection ("lumo" recognized)
- ✓ Semantic search (retrieving relevant chunks)

### 3. Run Live Interaction Test

Test with actual LLM responses:

```bash
python test_llm_responses.py
```

**Output**: 
- Real LLM inference with knowledge context
- Response latency (typically 30-50 seconds on CPU)
- Token counts and timing statistics

### 4. Run Full Voice Interface

Start the complete voice application:

```bash
python run.py
```

**Features**:
- Continuous listening for wake word "lumo"
- Automatic audio recording (stops after 3 seconds of silence)
- Full RAG pipeline with knowledge retrieval
- Real-time response generation
- Optional TTS (text-to-speech) output

## Voice Commands

After the wake word "lumo", you can ask:

### System Questions
- "How do you work?"
- "What is your architecture?"
- "Explain your design decisions"

### Memory Questions
- "How does memory work?"
- "What is the knowledge base?"
- "How do you learn?"

### Safety Questions
- "What are your safety features?"
- "How do you handle confirmations?"
- "What data do you store?"

### Action Requests
- "Save my conversation"
- "Search the web for..."
- "Remember that..."

## Audio Components

### Microphone Input
- **Device**: Automatically selects default input device
- **Sample Rate**: 16 kHz (standard for speech)
- **Duration**: 2-5 seconds per recording
- **Format**: Float32 mono audio

### Faster-Whisper (STT)
- **Model**: Base (74M parameters, high accuracy)
- **Compute**: INT8 quantization (faster, lower memory)
- **Language**: Automatic detection
- **Accuracy**: ~95% on clear speech

### Wake Word Detection
- **Wake Word**: "lumo" (case-insensitive)
- **Position**: Beginning of phrase ("lumo, what is...")
- **Detection**: Text-based (post-STT)
- **Sensitivity**: Exact match required

### Knowledge Retrieval (RAG)
- **Database**: FAISS (134 chunks, 384-dim embeddings)
- **Retrieval**: Top-k=2-3 most relevant chunks
- **Speed**: <100ms semantic search
- **Accuracy**: Relevant knowledge injected into LLM context

### LLM Inference
- **Backend**: Ollama
- **Model**: Llama 3.1 (8B or 70B)
- **Context**: 8192 tokens (supports long conversations)
- **Latency**: 30-50 seconds on CPU
- **Quantization**: Optional (4-bit, 8-bit available)

### Text-to-Speech (Optional)
- **TTS Engine**: Piper (if configured)
- **Quality**: Natural sounding voices
- **Speed**: Real-time synthesis
- **Languages**: Multiple supported

## Test Results

### Voice Demo Test
```
✓ Microphone input:        Available (9 devices)
✓ Knowledge base (RAG):    134 chunks loaded
✓ Wake word detection:     'lumo' recognized
✓ Command extraction:      Working
✓ Semantic search:         Retrieving chunks
✓ LLM integration:         Ready (when Ollama is running)
```

### Live LLM Test
```
✓ Ollama connection verified
✓ Available models: 3 (llama3.1:latest, llama3.1:8b, phi:latest)
✓ Knowledge base: 134 chunks indexed
✓ 4 test queries: All answered correctly
✓ Response latency: 30-48 seconds (normal for CPU)
✓ Knowledge grounding: Verified
```

## Example Interactions

### Interaction 1: System Knowledge
```
User: "Lumo, what is my memory system?"

[SYSTEM PROCESSING]
1. Wake word detected: ✓
2. Command extracted: "what is my memory system"
3. Knowledge retrieved: 2 chunks about MEMORY
4. RAG context injected into LLM
5. LLM response: "Your memory system uses FAISS to store and retrieve..."
```

### Interaction 2: Architecture Explanation
```
User: "Lumo, explain your design decisions"

[SYSTEM PROCESSING]
1. Wake word detected: ✓
2. Command extracted: "explain your design decisions"
3. Knowledge retrieved: 2 chunks from DESIGN_DECISIONS.txt
4. RAG context injected
5. LLM response: "I made several key design decisions..."
```

### Interaction 3: Safety Features
```
User: "Lumo, what are your safety features?"

[SYSTEM PROCESSING]
1. Wake word detected: ✓
2. Command extracted: "what are your safety features"
3. Knowledge retrieved: 2 chunks from SAFETY_GUARDRAILS.txt
4. RAG context injected
5. LLM response: "Safety features include confirmation gates, input validation..."
```

## Troubleshooting

### Issue: Ollama Connection Timeout
**Cause**: Ollama not running
**Solution**: 
```bash
ollama serve
```
**Check**: http://localhost:11434/api/tags should return model list

### Issue: Whisper Model Not Found
**Cause**: Faster-Whisper model not downloaded
**Solution**: 
```bash
python -c "from faster_whisper import WhisperModel; WhisperModel('base')"
```

### Issue: Microphone Not Detected
**Cause**: Audio driver issue
**Solution**: Check Windows Sound settings → Recording devices
**Fallback**: Test with `test_voice_demo.py` (demo mode)

### Issue: Poor Transcription Quality
**Causes**: 
- Background noise
- Unclear speech
- Microphone sensitivity too low

**Solutions**:
- Speak clearly and slowly
- Reduce background noise
- Check microphone levels in Windows Sound Settings

### Issue: LLM Response is Generic
**Cause**: Knowledge base not properly injected
**Solution**: 
1. Check knowledge base: `python -c "from knowledge.search import retrieve; print(retrieve('test', k=2))"`
2. Verify RAG: `python test_llm_responses.py`

## Advanced Configuration

### Adjust Wake Word
Edit `audio/stt.py`:
```python
def listen_continuous(timeout=30, wake_word="lumo"):  # Change "lumo"
```

### Change STT Model
Edit `audio/stt.py`:
```python
whisper_model = WhisperModel("base", compute_type="int8")  # Change "base" to "small", "medium", "large"
```

### Adjust RAG Retrieval K
Edit `core/llm.py`:
```python
return ask_llm_with_knowledge(query, messages=None, k=3)  # Change k=3
```

### Switch LLM Model
Edit `core/llm.py`:
```python
payload = {
    "model": "llama3.1",  # Change to "phi", "llama3.1:8b", etc.
    ...
}
```

## Files Involved

```
VOICE INTERFACE FILES:
├── audio/stt.py              # Speech-to-text with VAD
├── core/llm.py               # LLM with RAG augmentation
├── knowledge/search.py       # Semantic search
├── knowledge/rag.py          # RAG message augmentation

TEST FILES:
├── test_voice_demo.py        # Voice interface demo
├── test_voice.py             # Full voice test (requires Faster-Whisper)
├── test_llm_responses.py     # Live LLM testing

CONFIGURATION:
├── config.py                 # System configuration
├── requirements.txt          # Python dependencies
```

## Dependencies

### Required
- `ollama` - LLM backend (external)
- `faster-whisper` - Speech-to-text
- `sounddevice` - Audio input/output
- `scipy` - Audio file handling
- `faiss` - Vector search (already installed)
- `sentence-transformers` - Embeddings (already installed)

### Optional
- `webrtcvad` - Voice activity detection (requires C++ build tools)
- `piper-tts` - Text-to-speech synthesis

### Install Audio Dependencies
```bash
pip install faster-whisper scipy sounddevice
```

**Note**: `webrtcvad` requires Microsoft C++ Build Tools

## Performance Metrics

| Component | Metric | Value |
|-----------|--------|-------|
| Microphone Detection | Latency | < 1ms |
| Audio Recording | Time | 2-5 seconds |
| STT (Faster-Whisper) | Latency | 3-8 seconds |
| Wake Word Detection | Time | < 100ms |
| Knowledge Retrieval | Time | < 100ms |
| LLM Inference | Latency | 30-50 seconds (CPU) |
| TTS Synthesis | Time | 1-3 seconds |
| **Total Interaction** | Time | ~40-60 seconds |

## Next Steps

1. **Install Ollama** if not already installed
2. **Run voice demo**: `python test_voice_demo.py`
3. **Test with LLM**: `python test_llm_responses.py`
4. **Start voice interface**: `python run.py`
5. **Train on voice commands**: Create custom intents

## Support

For issues or questions:
1. Check **Troubleshooting** section above
2. Run diagnostic: `python test_voice_demo.py`
3. Check logs: `memory/conversation_history.json`
4. Review knowledge base: `knowledge/raw/`

---

**Status**: ✅ Voice interface fully operational and tested
**Last Updated**: January 2025
**Components**: All green (Ollama required for live inference)
