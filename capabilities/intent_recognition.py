import json
import re

# Load intents from the intents.json file
def load_intents(file_path='knowledge/intents.json'):
    with open(file_path, 'r') as file:
        intents = json.load(file)
    return intents

# Function to recognize intent using regular expressions
def recognize_intent(text, intents):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if re.search(pattern, text, re.IGNORECASE):
                print(f"Matched pattern: {pattern} for intent: {intent['tag']}")  # Debugging line
                return intent
    print(f"No match found for input: {text}")  # Debugging line
    return None
