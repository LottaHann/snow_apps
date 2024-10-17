import spacy
import json
import os
from nltk.metrics import jaccard_distance
import random

# Ladda spaCy-modellen
nlp = spacy.load("en_core_web_sm")

# Ladda intents.json från samma katalog som skriptet
def load_intents():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Hitta katalogen där skriptet körs
    intents_file_path = os.path.join(script_dir, 'intents.json')  # Använd relativ sökväg

    with open(intents_file_path, 'r') as file:
        intents = json.load(file)
    return intents

# Funktion för att beräkna jaccard-similaritet mellan input och mönster
def jaccard_similarity(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    tokens1 = set([token.lemma_ for token in doc1 if not token.is_stop])
    tokens2 = set([token.lemma_ for token in doc2 if not token.is_stop])

    distance = jaccard_distance(tokens1, tokens2)
    return 1 - distance

# Funktion för att få ett svar baserat på användarinmatning
def make_ask_response(user_input):
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
        return "Sorry, I don't understand that."

# Funktion för att få svaret baserat på användarinmatning
def get_ask(user_input):
    response = make_ask_response(user_input)
    return response

# Om du vill testa funktionen direkt
if __name__ == "__main__":
    user_input = "hello"  # Eller vilken fråga du vill testa
    response = get_ask(user_input)
    print(f"Bot: {response}")
