def handle_memory(context_manager, intent, entities):
    if intent == 'feedback':
        return  # Skip updating memory for feedback to avoid storing correction process
    for entity in entities:
        context_manager.update_context('memory', {entity[1]: entity[0]})
