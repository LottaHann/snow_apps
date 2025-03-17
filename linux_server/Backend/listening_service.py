import speech_recognition as sr
import datetime

from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from log_funcs import log_started_listening, log_callback, log_stop_listening, log_search_answer, log_answer_found, log_answer_play, log_call_ended, log_sr_error, log_type
from text_processing_service import text_exit_match
from nltk_model.get_ask import make_ask_response, hotword_detection

tts_engine = TextToSpeechEngine()
r = sr.Recognizer()
m = sr.Microphone()
stop_listening = None
user_input = ""
status = "off"

def exit_listening():
    """
    Exit listening for audio input.
    
    """
    print("exiting listening")
    global stop_listening
    global user_input
    if stop_listening is not None:
        stop_listening(wait_for_stop=False)
        stop_listening = None
        log_stop_listening(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("stopped listening")

    #wait until the callback is done
    

    q = user_input
    a = ""

    if q == "":
        a = "Sorry, I could not understand audio."
    elif text_exit_match(q):
        a = "Thank you for using our robot app. The application is now exiting."
    else:
        log_search_answer(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        a = make_ask_response(q)
        #hotword detection: switch to actual hotword not jaccard

    log_answer_found(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("answer: " + a)
    log_answer_play(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Thread(tts_engine.speak(a, "Female"))
    log_call_ended(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    user_input = ""




def callback(r, audio):
    """
    STT Callback function for listen in background.

    :param r: Recognizer instance.
    :param audio: Audio data to be processed.
    """
    global status

    log_callback(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("in callback function")

    try:
        text = r.recognize_faster_whisper(audio, language="en")
        print("You said: " + text)
        global user_input
        user_input += text
        print("user_input: " + user_input)

    except sr.UnknownValueError as e:
        log_sr_error(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), e)

    if status == "off":
        exit_listening()
        


def start_listening():
    """
    Start listening for audio input.
    """
    log_type("speech")
    global stop_listening
    with m as source:
        r.adjust_for_ambient_noise(source)

    log_started_listening(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    stop_listening = r.listen_in_background(m, callback)
    
    print("listening...")

def set_status(s):
    global status
    status = s


def main():
    input_str = ""
    while input_str != "exit":
        input_str = input("enter command on off or exit: ")

        if input_str == "on":
            set_status("on")
            start_listening()
            print("started listening")

        elif input_str == "off":
            set_status("off")
            print("status off")


if __name__ == "__main__":
    main()
    


