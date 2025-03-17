
from pvrecorder import PvRecorder
import wave
import struct
import os
import threading
import datetime
from faster_whisper import WhisperModel
from ws_utils import broadcast_status



# Set working directory
os.chdir("/home/snow/Documents/snow_apps/linux_server/Backend")

# Initialize recorder
audio = []
AUDIO_PATH = "./test_transcription/audiofiles/wavfile.wav"
recorder = PvRecorder(frame_length=512)
transcribe_time = 0
recording = False
recorder_thread = None
# Load Faster Whisper Model
model = WhisperModel("small", device="cpu", compute_type="int8")


def record_audio():
    """Background thread function to capture audio."""
    global audio
    audio = []  # Reset audio buffer
    recorder.start()
    broadcast_status("listening")
    print("🎙️ Recording... Type 'off' to stop.")


    while recording:
        frame = recorder.read()
        audio.extend(frame)

    broadcast_status("processing")
    recorder.stop()
    save_audio()
    transcribe()

def save_audio():
    """Saves recorded audio to a WAV file."""
    print("🛑 Recording stopped. Saving file...")
    with wave.open("./test_transcription/audiofiles/wavfile2.wav", 'w') as f:
        f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
        f.writeframes(struct.pack("h" * len(audio), *audio))
    print(f"✅ Audio saved to {AUDIO_PATH}")

def transcribe():
    global transcribe_time
    start_time = datetime.datetime.now()
    """Transcribes the saved WAV file using Faster Whisper."""
    print("📝 Transcribing...")
    segments, _ = model.transcribe(AUDIO_PATH)
    
    transcription = " ".join(segment.text for segment in segments)
    transcribe_time = (datetime.datetime.now() - start_time).total_seconds()
    print(f"✅ Transcription complete. Time taken: {transcribe_time:.2f} seconds.")
    print(f"📝 Transcription: {transcription}")
    return transcription

def stop_recording():
    """Stops the recording thread."""
    global recording, recorder_thread
    if recording:
        recording = False
        if recorder_thread:
            recorder_thread.join()
            print("🛑 Recording stopped.")
    else:
        print("⚠️ Not currently recording.")

def init_recording():
    global recording, recorder_thread
    if not recording:
        recording = True
        recorder_thread = threading.Thread(target=record_audio, daemon=True)
        recorder_thread.start()
        print("🎙️ Recording started.")
    else:
        print("⚠️ Already recording!")

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
            break

        else:
            print("❌ Invalid command. Use 'on', 'off', or 'exit'.")

if __name__ == "__main__":
    main()
