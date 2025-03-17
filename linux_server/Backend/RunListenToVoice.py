import sys
from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from nltk_model.get_ask import make_ask_response, hotword_detection
import speech_recognition as sr
import os
import time
from datetime import datetime


# Lägg till sökvägen till din Flask-applikation
sys.path.append('D:/2024/Arcada robot/ArcadaRobot/Linux/Flask')
# Initiera Text-to-Speech motorn
tts_engine = TextToSpeechEngine()
# Global variabel för att styra programflödet
callIsOpen = True

stop_listening = None

r = sr.Recognizer()
m = sr.Microphone()

def log_audio_recognized(time):
    """
    Log the time when audio is recognized.
    
    :param time: The time when audio is recognized.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Audio recognized: {time}, ")

def log_stop_listening(time):
    """
    Log the time when stop_listening is called.
    
    :param time: The time when stop_listening is called.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"stop_listening called at: {time}, ")

def log_callback(time):
    """
    Log the time when the callback function is called.
    
    :param time: The time when the callback function is called.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Callback called at: {time}, ")

def log_search_answer(time):
    """
    Log the time when searching for an answer.
    
    :param time: The time when searching for an answer.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Find answer: {time}, ")

def log_answer_found(time):
    """
    Log the time when an answer is found.
    
    :param time: The time when an answer is found.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Answer found: {time}, ")

def log_started_listening(time):
    """
    Log the time when the system starts listening.
    
    :param time: The time when the system starts listening.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Started listening: {time}, ")

def log_answer_play(answer_time):
    """
    Log the time when the answer is played.
    
    :param answer_time: The time when the answer is played.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Answer played: {answer_time}, ")

def log_call_ended(end_time):
    """
    Log the time when the call ends.
    
    :param end_time: The time when the call ends.
    """
    with open("response_times.log", "a") as log_file:
        log_file.write(f"Call ended: {end_time}")

# Funktion för att dela upp ord från en given text
def splitWords(textinput):
    """
    Split the input text into words.
    
    :param textinput: The input text to be split.
    :return: A list of words.
    """
    return textinput.split()  # Dela upp texten i ord

# Kontrollera om användarens input innehåller ett avslutningsord
def text_exit_match(userInput):
    """
    Check if the user's input contains an exit command.
    
    :param userInput: The user's input text.
    :return: True if an exit command is found, False otherwise.
    """
    exit_list = ["out", "end", "exit", "bye", "goodbye", "stop", "close", "off"]
    userInput = splitWords(userInput)

    for attempt in exit_list:
        if attempt in userInput:
            print(f"Exit command detected: {attempt}")
            return True  # Avslutningsord har hittats
    return False

# Funktion för att hämta svar från chatbotten
def get_answer(input):
    """
    Get a response from the chatbot based on the user's input.
    
    :param input: The user's input text.
    :return: The chatbot's response.
    """
    if text_exit_match(input):
        hotword_detection(input)
        return input

    response = make_ask_response(input)  # Anropa get_ask-funktionen
    log_answer_found(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    hotword_detection(input)
    print(response)
    log_answer_play(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Thread(tts_engine.speak(response, "Female"))  # Säg svaret med TTS
    log_call_ended(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return response

# Funktion för att stoppa samtalet
def stopCall():
    """
    Stop the ongoing call.
    """
    global stop_listening
    if stop_listening:
        stop_listening()
        print("stopped listening")
        stop_listening = None
    else:
        print("stop_listening is None")


def callback(r, audio):
    """
    Callback function to process the audio input.
    
    :param r: Recognizer instance.
    :param audio: Audio data to be processed.
    """
    log_callback(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("in callback function")

    try:
        text = r.recognize_faster_whisper(audio, language="en")
        log_audio_recognized(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        log_search_answer(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    """
    Listen to the user's voice commands.
    """
    global stop_listening
    print("starting listening...")

    with m as source:
        r.adjust_for_ambient_noise(source)
    
    log_started_listening(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

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

