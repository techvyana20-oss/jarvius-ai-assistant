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
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

            command = recognizer.recognize_google(audio)
            print("🧠 Heard:", command)
            return command.lower()

    except sr.WaitTimeoutError:
        # Silence is normal → do nothing
        return ""

    except sr.UnknownValueError:
        print("❌ Could not understand")
        return ""

    except sr.RequestError:
        print("❌ Network issue")
        return ""

    except Exception as e:
        print("❌ Voice error:", e)
        return ""
