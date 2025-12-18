import subprocess


def speak(text):
    subprocess.run(
        [
            "audio/piper/piper.exe",
            "--model",
            "audio/piper/en_US-lessac-medium.onnx",
        ],
        input=text.encode(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
