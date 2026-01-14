import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 160)

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.8

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)

        try:
            command = recognizer.recognize_google(audio)
            print("🧠 Heard:", command)
            return command.lower()
        except:
            return ""
