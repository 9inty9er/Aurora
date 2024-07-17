import random
from capabilities.weather import get_weather

def generate_response(context_manager, intent, memory, entities):
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
    elif memory:
        memory_response = ", ".join([f"{k}: {', '.join(v)}" for k, v in memory.items()])
        return f"I remember you mentioned: {memory_response}. {random.choice(intent['responses'])}"
    else:
        return random.choice(intent['responses'])
