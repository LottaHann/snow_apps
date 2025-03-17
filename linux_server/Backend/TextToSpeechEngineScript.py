import pyttsx3
import threading

class Thread(threading.Thread):
    """
    A class to create and start a new thread.
    """
    def __init__(self, t, *args):
        """
        Initialize the thread with a target function and arguments.
        
        :param t: Target function to run in the thread.
        :param args: Arguments to pass to the target function.
        """
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

class TextToSpeechEngine:
    """
    A class to handle text-to-speech operations.
    """
    def __init__(self):
        """
        Initialize the text-to-speech engine and a threading lock.
        """
        self.engine = pyttsx3.init()
        self.engine._inLoop = False
        self.lock = threading.Lock()

    def speak(self, text, gender):
        """
        Convert text to speech with the specified gender voice.
        
        :param text: Text to be spoken.
        :param gender: Gender of the voice ('Male' or 'Female').
        """
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
        """
        Stop the text-to-speech engine.
        """
        self.engine.stop()