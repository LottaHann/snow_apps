import sys
from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from nltk_model.get_ask import make_ask_response, hotword_detection
import speech_recognition as sr
import os
import time


# Lägg till sökvägen till din Flask-applikation
sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask')
# Initiera Text-to-Speech motorn
tts_engine = TextToSpeechEngine()
# Global variabel för att styra programflödet
callIsOpen = True

stop_listening = None

r = sr.Recognizer()
m = sr.Microphone()

# Funktion för att dela upp ord från en given text
def splitWords(textinput):
    return textinput.split()  # Dela upp texten i ord

# Kontrollera om användarens input innehåller ett avslutningsord
def text_exit_match(userInput):
    exit_list = ["out", "end", "exit", "bye", "goodbye", "stop", "close", "off"]
    userInput = splitWords(userInput)

    for attempt in exit_list:
        if attempt in userInput:
            print(f"Exit command detected: {attempt}")
            return True  # Avslutningsord har hittats
    return False

# Funktion för att hämta svar från chatbotten
def get_answer(input):
    if text_exit_match(input):
        hotword_detection(input)
        return input

    response = make_ask_response(input)  # Anropa get_ask-funktionen
    hotword_detection(input)
    print(response)
    Thread(tts_engine.speak(response, "Female"))  # Säg svaret med TTS
    return response

# Funktion för att stoppa samtalet
def stopCall():
    global stop_listening
    if stop_listening:
        stop_listening()
        print("stopped listening")
        stop_listening = None
    else:
        print("stop_listening is None")


def callback(r, audio):
    print("in callback function")

    try:
        text = r.recognize_faster_whisper(audio, language="en")
        print("You said: " + text)
        if text == "":
            t = "Sorry, I could not understand audio."
            Thread(tts_engine.speak(t, "Female"))
            print(t)
            stopCall()
            return

        if text_exit_match(text):
            t = "Thank you for using our robot app. The application is now exiting."
            Thread(tts_engine.speak(t, "Female"))
            stopCall()
            return
        
        get_answer(text)
        
    except sr.UnknownValueError:

        t = "Sorry, I could not understand audio."
        # error_list.append(t)
        Thread(tts_engine.speak(t, "Female"))
        print(t)
        stopCall()
        return
            
        
    except sr.RequestError as e:
        t = "Could not request results from the Speech Recognition service."
        Thread(tts_engine.speak(t, "Female"))
        print(t)
        stopCall()
        return

    except Exception as e:
        print("Error:", e)
        stopCall()
        return


    


# Lyssna på användarens röstkommandon
def listen_to_voice():
    global stop_listening
    print("starting listening...")

    with m as source:
        r.adjust_for_ambient_noise(source)

    stop_listening = r.listen_in_background(m, callback)

    print("stop_listening: ", stop_listening)
    print("listening")

    

# Om du vill testa funktionen direkt
# Testa med en direktfråga
if __name__ == "__main__":
    #get_answer("Arcada")
    listen_to_voice()
    for _ in range(50): time.sleep(0.1)
    stopCall()
    for _ in range(200): time.sleep(0.1)

