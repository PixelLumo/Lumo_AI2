from audio.stt import transcribe_audio
from audio.tts import speak_text
from audio.vad import listen_for_speech
from core.llm import generate_response
from core.memory import Memory
from core.confirmation import confirm_action

memory = Memory()

def main():
    print("Lumo AI Voice Interface Started. Say 'exit' to quit.")
    while True:
        audio_data = listen_for_speech()
        if not audio_data:
            continue
        text = transcribe_audio(audio_data)
        if text.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Generate response from LLM
        response = generate_response(text, memory)
        speak_text(response)
        memory.add(text, response)

if __name__ == "__main__":
    main()
