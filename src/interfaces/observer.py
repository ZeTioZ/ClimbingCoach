from abc import ABC, abstractmethod
from interfaces.observable import Observable


class Observer(ABC):
    @abstractmethod
    def update(self, event_type, observable: Observable, *args, **kwargs):
        pass