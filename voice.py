import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 160)

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True

MIC_INDEX = 0   # ✅ hw:0,0

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    try:
        with sr.Microphone(device_index=MIC_INDEX) as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)

            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=5
            )

            command = recognizer.recognize_google(audio)
            print("🧠 Heard:", command)
            return command.lower()

    except sr.UnknownValueError:
        print("❌ Heard sound but could not understand")
        return ""

    except sr.RequestError as e:
        print("❌ Google API / Internet error:", e)
        return ""

    except Exception as e:
        print("❌ Voice error:", e)
        return ""
