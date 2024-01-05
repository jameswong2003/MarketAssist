import speech_recognition as sr

def speech_to_string():
    """
    Turn audio into text
    """
    recorder = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Say something...")
            audio = recorder.listen(source)

        text = recorder.recognize_google(audio)
        return text
    except sr.UnknownValueError():
        return ""
    
