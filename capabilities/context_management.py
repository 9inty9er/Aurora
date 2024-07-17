import json
import os

class ContextManager:
    def __init__(self):
        self.context = {
            'intent': [],
            'entities': []
        }
        self.memory = {}
        self.identity = self.load_backstory('knowledge/backstory.json')
        self.memory_file = 'knowledge/memory.json'
        self.load_memory()

    def load_backstory(self, file_path):
        with open(file_path, 'r') as file:
            backstory = json.load(file)
        return backstory

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump({'context': self.context, 'memory': self.memory}, file, indent=4)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                data = json.load(file)
                self.context = data.get('context', self.context)
                self.memory = data.get('memory', self.memory)

    def update_context(self, key, value):
        if key == 'intent':
            self.context['intent'].append(value)
        elif key == 'entities':
            self.context['entities'].append(value)
        elif key == 'memory':
            for k, v in value.items():
                if k in self.memory:
                    if v not in self.memory[k]:
                        self.memory[k].append(v)
                else:
                    self.memory[k] = [v]
        self.save_memory()

    def get_context(self):
        return self.context
    
    def get_memory(self):
        return self.memory
    
    def get_identity(self):
        return self.identity

    def clear_context(self):
        self.context = {
            'intent': [],
            'entities': []
        }
        self.save_memory()

    def retrieve_memory(self, entity_type):
        return self.memory.get(entity_type, [])

