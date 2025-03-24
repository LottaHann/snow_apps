from pvrecorder import PvRecorder
import wave
import struct
import os
import threading
import datetime
from faster_whisper import WhisperModel
import asyncio
import json
import sys
from TextToSpeechEngineScript import TextToSpeechEngine, Thread
from nltk_model.get_ask import make_ask_response, hotword_detection
from text_processing_service import text_exit_match
from log_funcs import log_started_listening, log_stop_listening, log_search_answer, log_answer_found, log_answer_play, log_call_ended, log_transcription_time

event_loop = None  
clients = set()
tts_engine = TextToSpeechEngine()

def get_clients():
    return clients

def add_client(client):
    clients.add(client)


def remove_client(client):
    clients.remove(client)


def set_event_loop(loop):
    """Set the event loop from the WebSocket server."""
    global event_loop
    event_loop = loop

def broadcast_status(status):
    """Sends status updates to all WebSocket clients."""
    message = json.dumps({"status": status})
    
    future = asyncio.run_coroutine_threadsafe(send_to_all_clients(message), event_loop)
    future.result()


async def send_to_all_clients(message):
    clients = get_clients()
    if clients:
        print(f"📢 Sending message to clients: {message}")  # Debug print
        await asyncio.wait([client.send(message) for client in clients])
    else:
        print("⚠️ No connected clients.")


# Initialize recorder
audio = []
AUDIO_PATH = "./audiofiles/wavfile.wav"
recorder = PvRecorder(frame_length=512)
transcribe_time = 0
recording = False
recorder_thread = None
# Load Faster Whisper Model
model = WhisperModel("small", device="cpu", compute_type="int8")


def record_audio():
    print("in record_audio")
    """Background thread function to capture audio."""
    global audio
    audio = []  # Reset audio buffer
    recorder.start()
    try:
        recorder.start()
        log_started_listening(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("🎙️ Recording... Type 'off' to stop.") 

        print("recording: ", recording)
        while recording:
            frame = recorder.read()
            audio.extend(frame)
            
            try:
                broadcast_status("listening")
            except Exception as e:
                print(f"❌ Error sending status to clients: {e}")
            
        print("Exited while loop")
        recorder.stop()
        log_stop_listening(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        
        try:
            broadcast_status("processing")
        except Exception as e:
            print(f"❌ Error sending status \'processing\' to clients: {e}")
        
        recorder.stop()
        save_audio()
        transcribe()
    
    except Exception as e:
        print(f"❌ Error in recording thread: {e}")
    
def save_audio():
    """Saves recorded audio to a WAV file."""
    print("🛑 Recording stopped. Saving file...")
    with wave.open("./audiofiles/wavfile.wav", 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    print(f"✅ Audio saved to {AUDIO_PATH}")

def transcribe():
    global transcribe_time
    start_time = datetime.datetime.now()
    """Transcribes the saved WAV file using Faster Whisper."""
    print("📝 Transcribing...")
    transcription = ""
    
    
    segments, _ = model.transcribe(AUDIO_PATH)
    transcription = " ".join(segment.text for segment in segments)
    
    
    transcribe_time = (datetime.datetime.now() - start_time).total_seconds()
    print(f"✅ Transcription complete. Time taken: {transcribe_time:.2f} seconds.")
    log_transcription_time(transcribe_time)
    
    print(f"📝 Transcription: {transcription}")
    respond(transcription, "speech")
    return

def respond(text, type):
    """
    Respond to the user's query.
    
    :param text: The text to respond to.
    :param type: The type of question (speech or text).
    """
    hotword_detection(text)
    response = ""
    log_search_answer(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))    

    if text_exit_match(text):
        response = "Thank you for using our robot app. The application is now exiting."
    elif text == "":
        response = "Sorry, I could not understand audio."
    else:
        response = make_ask_response(text)

    log_answer_found(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if type == "speech":
        broadcast_status("responding")


    log_answer_play(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    Thread(tts_engine.speak(response, "Female"))
    log_call_ended(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    if type == "speech":
        broadcast_status("responding")

    return text

def stop_recording():
    """Stops the recording thread."""
    global recording, recorder_thread
    if recording:
        recording = False
        print("🛑 Recording stopped.")
    else:
        print("⚠️ Not currently recording.")

def init_recording():
    global recording, recorder_thread
    if not recording:
        print("🟢 Starting recording thread...")
        recording = True
        try:
            recorder_thread = threading.Thread(target=record_audio, daemon=True)
            recorder_thread.start()
            print("🎙️ Recording started.")
        except Exception as e:
            print(f"❌ Error starting recording thread: {e}")
    else:
        print("⚠️ Already recording!")

def stop_talking():
    tts_engine.stop()



def main():
   
    while True:
        command = input("Enter 'on' to start, 'off' to stop, or 'exit' to quit: ").strip().lower()

        if command == "on":
            init_recording()

        elif command == "off":
            stop_recording()

        elif command == "exit":
            print("👋 Exiting...")
            recorder.delete()
            stop_talking()
            break

        else:
            print("❌ Invalid command. Use 'on', 'off', or 'exit'.")

if __name__ == "__main__":
    main()
