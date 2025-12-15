import pyttsx3
import config

engine = pyttsx3.init()
engine.setProperty('voice', config.SETTINGS['voice'])

def speak(text):
    engine.say(text)
    engine.runAndWait()
