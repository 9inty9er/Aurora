import json
import random
from transformers import pipeline
from capabilities.entity_extraction import extract_entities
from capabilities.context_management import ContextManager
from capabilities.weather import get_weather
from capabilities.intent_recognition import load_intents, recognize_intent

# Load Hugging Face model
chatbot = pipeline('text2text-generation', model='facebook/blenderbot-400M-distill')

# Load intents
intents = load_intents('knowledge/intents.json')

# Initialize context manager
context_manager = ContextManager()

# Function to preprocess text with spaCy
import spacy
nlp = spacy.load('en_core_web_sm')

def preprocess_text(text):
    doc = nlp(text)
    preprocessed_text = ' '.join([token.text for token in doc])  # Use token.text to retain original words
    return preprocessed_text

# Function to chat with Aurora
def chat_with_aurora():
    print("Start chatting with Aurora (type 'exit' to stop):")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        preprocessed_input = preprocess_text(user_input)
        print(f"Preprocessed Input: {preprocessed_input}")  # Debugging line
        intent = recognize_intent(preprocessed_input, intents)
        if intent:
            print(f"Recognized intent: {intent['tag']}")  # Debugging line
            if intent['tag'] == 'weather':
                response = get_weather()
            else:
                response = random.choice(intent['responses'])
            context_manager.update_context('intent', intent['tag'])
        else:
            print("No recognized intent, using chatbot model")  # Debugging line
            response = chatbot(preprocessed_input, max_length=50, num_return_sequences=1, truncation=True)[0]['generated_text'].strip()
            context_manager.update_context('intent', 'unknown')
        
        # Extract and print entities
        entities = extract_entities(user_input)
        if entities:
            context_manager.update_context('entities', entities)
            print(f"Extracted Entities: {entities}")

        print(f"Aurora: {response}")
        print(f"Context: {context_manager.get_context()}")

# Start chatting
chat_with_aurora()
