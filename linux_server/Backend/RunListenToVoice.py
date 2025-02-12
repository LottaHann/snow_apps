import sys
from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from nltk_model.get_ask import make_ask_response, hotword_detection
import speech_recognition as sr
import os


# Lägg till sökvägen till din Flask-applikation
sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask')
# Initiera Text-to-Speech motorn
tts_engine = TextToSpeechEngine()
# Global variabel för att styra programflödet
callIsOpen = True

recognizer = sr.Recognizer()

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
    global callIsOpen
    callIsOpen = False

# Lyssna på användarens röstkommandon
def listen_to_voice():
    global callIsOpen
    callIsOpen = True
    error_list = []


    while callIsOpen:
        print("Listening...")
        
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        
        
        """
        # check if test.wav file can be found:
        if not os.path.exists("test.wav"):
            print("test.wav file not found")
            stopCall()
            break
        else:
            print("wav file found")

        with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
            audio = recognizer.record(source) 
            print("recorded wav file")   
        """          
        
        try:
            print("Processing audio...")
            text = recognizer.recognize_faster_whisper(audio, language="en")
            print("You said:", text)

            if text == "":
                t = "Sorry, I could not understand audio."
                Thread(tts_engine.speak(t, "Female"))
                print(t)
                stopCall()
                break

            if text_exit_match(text):
                t = "Thank you for using our robot app. The application is now exiting."
                Thread(tts_engine.speak(t, "Female"))
                stopCall()
                break
            
            get_answer(text)
        
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

        except Exception as e:
            print("Error:", e)
            stopCall()
            break

# Om du vill testa funktionen direkt
# Testa med en direktfråga
if __name__ == "__main__":
    get_answer("Arcada")

