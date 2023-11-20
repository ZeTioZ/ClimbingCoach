from abc import ABC

class Event(ABC):
    def __init__(self):
        self.listeners = []
        self.handlers = {}


    def register(self, listener):
        self.listeners.append(listener)
        for event_type in listener.event_types:
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(listener)


    def unregister(self, listener):
        self.listeners.remove(listener)
        for event_type in listener.event_types:
            if event_type in self.handlers:
                self.handlers[event_type].remove(listener)


    def has_listener(self, event_type):
        if event_type in self.handlers:
            return len(self.handlers[event_type]) > 0
        return False


    def notify(self, event_types = [], *args, **kwargs):
        if len(event_types) > 0:
            for event_type in event_types:
                if event_type in self.handlers:
                    for listener in self.handlers[event_type]:
                        listener.update(self, [event_type], *args, **kwargs)
        else:
            self.notify_all(self, *args, **kwargs)


    def notify_all(self, *args, **kwargs):
        for listener in self.listeners:
            listener.update(self, self.handlers.keys(), *args, **kwargs)
