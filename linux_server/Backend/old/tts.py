from MeloTTS.melo.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import nltk
nltk.download('averaged_perceptron_tagger_eng')


speed = 1.0

device = 'auto' 
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id
output_path = 'output.wav'

def tts(text: str, lang: str):
    """
    Convert text to speech using the MeloTTS API.
    
    :param text: The text to convert to speech.
    :param lang: The language of the text.
    :return: The speech audio.
    """
    model.tts_to_file(text, speaker_ids['EN-US'], output_path, speed=speed)
    play_audio()


def play_audio():
    """
    Play the audio in separate thread.
    
    :param audio: The audio to play.
    """
    audio = AudioSegment.from_file(output_path)
    play(audio)
    