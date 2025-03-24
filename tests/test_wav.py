import speech_recognition as sr

def test_wav():
    r = sr.Recognizer()
    with sr.WavFile("test.wav") as source:              # use "test.wav" as the audio source
        audio = r.record(source)                        # extract audio data from the file

    try:
        print("Transcription: " + r.recognize_whisper(audio, language="english"))   # recognize speech using Google Speech Recognition
    except LookupError:                                 # speech is unintelligible
        print("Could not understand audio")


if __name__ == "__main__":
    test_wav()