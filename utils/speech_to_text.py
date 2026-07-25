import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone(device_index=2) as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return None

    except Exception as e:
        print(e)
        return None