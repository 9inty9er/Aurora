class ContextManager:
    def __init__(self):
        self.context = {}

    def update_context(self, key, value):
        if key in self.context:
            if isinstance(self.context[key], list):
                self.context[key].append(value)
            else:
                self.context[key] = [self.context[key], value]
        else:
            self.context[key] = value

    def get_context(self):
        return self.context

    def clear_context(self):
        self.context = {}
