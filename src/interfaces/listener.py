from abc import ABC, abstractmethod

from interfaces.event import Event
from enums.event_type import EventType


class Listener(ABC):
    def __init__(self, event_types) -> None:
        super().__init__()
        self.event_types: EventType = event_types


    @abstractmethod
    def update(self, observable: Event, event_types: [EventType] = [], *args, **kwargs):
        pass