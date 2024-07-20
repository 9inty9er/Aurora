import json
import threading
import spacy
from transformers import pipeline
from capabilities.entity_extraction import extract_entities
from capabilities.context_management import ContextManager
from capabilities.intent_recognition import load_intents, recognize_intent
from capabilities.backup import start_backup_process, start_periodic_backup_thread
from capabilities.memory import handle_memory
from capabilities.response import generate_response

# Load Hugging Face model
chatbot = pipeline('text2text-generation', model='facebook/blenderbot-400M-distill')

# Load intents
intents = load_intents('knowledge/intents.json')

# Initialize context manager
context_manager = ContextManager()

# Function to preprocess text with spaCy
nlp = spacy.load('en_core_web_lg')

def preprocess_text(text):
    doc = nlp(text)
    preprocessed_text = ' '.join([token.text for token in doc])
    return preprocessed_text

# Function to chat with Aurora
def chat_with_aurora():
    print("Start chatting with Aurora (type 'exit' to stop):")
    # Start the initial backup check
    start_backup_process()
    # Schedule periodic backups
    start_periodic_backup_thread()

    identity = context_manager.get_identity()
    print(f"Hello, I am {identity['identity']['name']}, an advanced AI developed to assist and learn from human interactions.")
    print(f"Here's a bit about me: {identity['backstory']['creation']}")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            preprocessed_input = preprocess_text(user_input)
            print(f"Preprocessed Input: {preprocessed_input}")

            # Check if awaiting feedback
            if context_manager.get_context().get('awaiting_feedback'):
                context_manager.update_context('awaiting_feedback', False)
                entities = extract_entities(user_input)
                for entity in entities:
                    context_manager.update_context('memory', {entity[1]: entity[0]})
                response = "Thank you for the correction. I've updated my memory."
            else:
                intent = recognize_intent(preprocessed_input, intents)
                if intent:
                    print(f"Recognized intent: {intent['tag']}")
                    entities = extract_entities(user_input)
                    if entities:
                        context_manager.update_context('entities', entities)
                        print(f"Extracted Entities: {entities}")
                        handle_memory(context_manager, intent['tag'], entities)

                    memory = context_manager.get_memory()
                    response = generate_response(context_manager, intent, memory, entities, user_input)

                    context_manager.update_context('intent', intent['tag'])
                else:
                    print("No recognized intent, using chatbot model")
                    response = chatbot(preprocessed_input, max_length=50, num_return_sequences=1, truncation=True)[0]['generated_text'].strip()
                    context_manager.update_context('intent', 'unknown')

            if "siblings" in response or "job" in response:
                response = "I am an AI and do not have siblings or a job in the traditional sense."

            print(f"Aurora: {response}")
            print(f"Context: {context_manager.get_context()}")
            print(f"Memory: {context_manager.get_memory()}")
        except Exception as e:
            print(f"Error during interaction: {e}")

# Start chatting
chat_with_aurora()
