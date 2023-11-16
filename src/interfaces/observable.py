from abc import ABC

class Observable(ABC):
    def __init__(self):
        self.observers = []


    def register(self, observer):
        self.observers.append(observer)


    def notify(self, event_type, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, event_type, *args, **kwargs)