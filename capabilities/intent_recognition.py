import re
import json  # Import the json module

def load_intents(file_path):
    with open(file_path, 'r') as file:
        intents = json.load(file)
    return intents['intents']

def recognize_intent(text, intents):
    for intent in intents:
        for pattern in intent['patterns']:
            # Use regex to make pattern matching more flexible
            if re.search(r'\b' + re.escape(pattern.lower()) + r'\b', text.lower()):
                print(f"Matched pattern: '{pattern}' for intent: '{intent['tag']}' with text: '{text}'")
                return intent
    print(f"No match found for input: '{text}'")
    return None
