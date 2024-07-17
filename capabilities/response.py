import random
from capabilities.weather import get_weather

def generate_response(context_manager, intent, memory, entities, user_input):
    identity = context_manager.get_identity()
    if intent['tag'] == 'weather':
        city = None
        for entity in entities:
            if entity[1] == 'GPE':  # GPE (Geopolitical Entity) is used for cities
                city = entity[0]
                break
        if city:
            return get_weather(city)
        else:
            return get_weather()
    elif intent['tag'] == 'name':
        return f"My name is {identity['identity']['name']}."
    elif intent['tag'] == 'location':
        return f"I am an AI and I exist in the digital world. I am wherever you need me to be."
    elif intent['tag'] == 'feedback':
        # Ask for the correct information
        context_manager.update_context('awaiting_feedback', True)
        return "I'm sorry. Can you please tell me the correct information?"
    elif memory:
        memory_response = ", ".join([f"{k}: {', '.join(v)}" for k, v in memory.items()])
        return f"I remember you mentioned: {memory_response}. {random.choice(intent['responses'])}"
    else:
        return random.choice(intent['responses'])
