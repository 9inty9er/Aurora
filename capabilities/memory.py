def handle_memory(context_manager, intent, entities):
    for entity in entities:
        context_manager.update_context('memory', {entity[1]: entity[0]})
