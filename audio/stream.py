import sounddevice as sd
import queue

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())


def start_stream(sample_rate=16000):
    stream = sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        callback=audio_callback
    )
    stream.start()
    return stream
