from abc import ABC
from enums.flux_reader_enum import FluxReaderEnum

class Observable(ABC):
    def __init__(self):
        self.observers = []


    def register(self, observer):
        self.observers.append(observer)


    def notify(self, event_type: FluxReaderEnum, *args, **kwargs):
        for observer in self.observers:
            observer.update(self, event_type, *args, **kwargs)