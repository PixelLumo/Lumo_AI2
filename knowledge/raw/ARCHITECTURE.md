# LUMO AI System Architecture

## High-Level Design

LUMO is a JARVIS-style AI assistant built on modular, event-driven components.

```
┌─────────────────────────────────────────────────────────┐
│                   USER INTERFACE                         │
│        (Web UI / Voice / Text Input)                     │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              AUDIO LAYER (STT)                           │
│   Faster-Whisper + WebRTC VAD                           │
│   Wake word detection ("lumo")                          │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              CORE ORCHESTRATION                          │
│   • Query parsing                                       │
│   • Intent detection                                    │
│   • Action routing                                      │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼──┐    ┌─────▼────┐   ┌────▼──────┐
   │ MEMORY │    │   LLM    │   │ ACTIONS   │
   │ (FAISS)│    │ (Ollama) │   │ (Execute) │
   └────────┘    └──────────┘   └───────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │     LOGGING & LEARNING      │
        │   (Feedback loop)           │
        └─────────────────────────────┘
```

## Core Modules

### 1. Audio Layer (`audio/stt.py`)
- **Faster-Whisper**: Fast, offline speech-to-text
- **WebRTC VAD**: Voice activity detection (silence handling)
- **Wake word detection**: Listens for "lumo" trigger
- **Output**: Transcribed text + duration

### 2. LLM Integration (`core/llm.py`)
- **Backend**: Ollama (local LLM, no API keys)
- **Model**: Llama 3.1 (7B or larger)
- **RAG Support**: Knowledge augmentation via ask_llm_with_knowledge()
- **System Prompt**: JARVIS personality (concise, action-oriented)

### 3. Memory System (`core/memory.py`)
- **Vector DB**: FAISS (Facebook AI Similarity Search)
- **Embeddings**: SentenceTransformer (all-MiniLM-L6-v2)
- **Purpose**: Semantic search over conversation history
- **Storage**: JSON (conversation_history.json)

### 4. Action Execution (`core/planner.py`)
- **Supported actions**: web_search, save_note, execute_action
- **Confirmation gating**: Destructive actions require user approval
- **Logging**: All actions tracked for learning

### 5. State Management (`core/confirmation.py`)
- **Singleton**: One confirmation per session
- **Timeout**: 10 seconds to confirm/reject
- **Status tracking**: waiting, confirmed, rejected

### 6. Learning System (`learning/`)
- **Analysis**: Track success rates, wake word accuracy, failures
- **Auto-tuning**: Adjust thresholds based on performance
- **Feedback loop**: Continuous improvement

### 7. Logging (`core/logger.py`)
- **Session tracking**: Unique ID per run
- **Event logging**: Transcription, LLM calls, actions, errors
- **File format**: JSON for structured analysis

## Data Flow

```
Audio Input
    ↓ (STT)
Transcribed Text
    ↓ (Intent parsing)
Semantic Query
    ├→ Memory search (past context)
    ├→ Knowledge retrieval (RAG)
    └→ LLM inference
        ↓
LLM Response (text or action)
    ├→ Text output (TTS)
    └→ Action execution (if required)
        └→ Confirmation gate (if destructive)
            ↓
        Action result
            ↓
        Log & learn
```

## Key Design Principles

1. **Modularity**: Each component is independent, testable
2. **Locality**: No cloud dependencies (offline-first)
3. **Simplicity**: Minimal dependencies, clear data flow
4. **Auditability**: Everything is logged and traceable
5. **Learnability**: System improves from interactions
