import spacy
import json
import os
from nltk.metrics import jaccard_distance
import random
import requests
rpi_ip = "192.168.99.200"
expression_server = f'http://{rpi_ip}:5000'
update_expression_endpoint = f'{expression_server}/update_expression'

# Ladda spaCy-modellen
nlp = spacy.load("en_core_web_sm")

# Ladda intents.json från samma katalog som skriptet
def load_intents():
    """
    Load intents from the intents.json file.
    
    :return: A dictionary containing intents.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Hitta katalogen där skriptet körs
    intents_file_path = os.path.join(script_dir, 'intents.json')  # Använd relativ sökväg

    with open(intents_file_path, 'r') as file:
        intents = json.load(file)
    return intents

#Laod hotwords.json från samma katalog som skriptet
def load_hotwords():
    """
    Load hotwords from the hotwords.json file.
    
    :return: A dictionary containing hotwords.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Hitta katalogen där skriptet körs
    hotwords_file_path = os.path.join(script_dir, 'hotwords.json')  # Använd relativ sökväg

    with open(hotwords_file_path, 'r') as file:
        hotwords = json.load(file)
    return hotwords

# Funktion för att beräkna jaccard-similaritet mellan input och mönster
def jaccard_similarity(text1, text2):
    """
    Calculate the Jaccard similarity between two texts.
    
    :param text1: The first text.
    :param text2: The second text.
    :return: The Jaccard similarity score.
    """
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    tokens1 = set([token.lemma_ for token in doc1 if not token.is_stop])
    tokens2 = set([token.lemma_ for token in doc2 if not token.is_stop])

    distance = jaccard_distance(tokens1, tokens2)
    return 1 - distance

# Funktion för att få ett svar baserat på användarinmatning
def make_ask_response(user_input):
    """
    Get a response based on the user's input.
    
    :param user_input: The user's input text.
    :return: A response from the chatbot.
    """
    intents = load_intents()
    
    best_match = None
    highest_similarity = 0
    
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            similarity = jaccard_similarity(user_input, pattern)
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match = intent
    
    if best_match:
        # Om vi hittar en match, returnera ett slumpmässigt svar från responses
        return random.choice(best_match["responses"])
    else:
        #response = get_response(user_input)
        return "Sorry, I don't understand that."
        #return response

#Funktion för att hitta hotwords
def hotword_detection(user_input):
    """
    Detect hotwords in the user's input and update the expression server.
    
    :param user_input: The user's input text.
    """
    hotwords = load_hotwords()
    match = None

    for group in hotwords["hotwords"]:
        for hotword in group["patterns"]:
            if hotword in user_input:
                match = group
                break
    

    if match:
        # Uppdatera uttryck på servern
        data = {"expression": match["hotword"]}
        try:
            response = requests.post(update_expression_endpoint, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error updating expression: {e}")
    else:
        print("No hotword detected.")

# Om du vill testa funktionen direkt
if __name__ == "__main__":
    user_input = "hello"  # Eller vilken fråga du vill testa
    response = make_ask_response(user_input)
    print(f"Bot: {response}")
