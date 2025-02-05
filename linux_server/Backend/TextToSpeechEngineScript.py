import pyttsx3
import threading
class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

class TextToSpeechEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine._inLoop = False
        self.lock = threading.Lock()
    def speak(self, text, gender):
        with self.lock:
            voice_dict = {'Male': 0, 'Female': 1}
            code = voice_dict[gender]
            # Setting up voice rate
            self.engine.setProperty('rate', 125)
            # Setting up volume level between 0 and 1
            self.engine.setProperty('volume', 0.8)
            # Change voices: 0 for male and 1 for female
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[code].id)
            self.engine.say(text)
            self.engine.runAndWait() 
            self.engine.stop()
    def cleanup(self):
        self.engine.stop()