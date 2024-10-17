import sys
import speech_recognition as sr
from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from spacy_nltk_treings_modol.get_ask import get_ask

# Lägg till sökvägen till din Flask-applikation
sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask')
# Initiera Text-to-Speech motorn
tts_engine = TextToSpeechEngine()
# Global variabel för att styra programflödet
callIsOpen = True

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
def get_askRobot(input):
    if text_exit_match(input):
        return input

    response = get_ask(input)  # Anropa get_ask-funktionen
    print(response)
    Thread(tts_engine.speak(response, "Female"))  # Säg svaret med TTS
    return response

# Funktion för att stoppa samtalet
def stopCall():
    global callIsOpen
    callIsOpen = False

# Lyssna på användarens röstkommandon
def listen_to_voice():
    global callIsOpen
    callIsOpen = True

    recognizer = sr.Recognizer()
    error_list = []

    while callIsOpen:
        print("Listening...")
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)

            if text_exit_match(text):
                t = "Thank you for using our robot app. The application is now exiting."
                Thread(tts_engine.speak(t, "Female"))
                stopCall()
                break
            
            get_askRobot(text)
        
        except sr.UnknownValueError:

            t = "Sorry, I could not understand audio."
            # error_list.append(t)
            Thread(tts_engine.speak(t, "Female"))
            print(t)
            stopCall()
            break
            
        
        except sr.RequestError as e:
            t = "Could not request results from the Speech Recognition service."
            Thread(tts_engine.speak(t, "Female"))
            print(t)
            stopCall()
            break

# Om du vill testa funktionen direkt
# Testa med en direktfråga
if __name__ == "__main__":
    get_askRobot("Arcada")

