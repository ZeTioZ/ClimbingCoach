from abc import ABC, abstractmethod
from enums.flux_reader_enum import FluxReaderEnum
from observable import Observable


class Observer(ABC):
    @abstractmethod
    def update(self, event_type: FluxReaderEnum, observable: Observable, *args, **kwargs):
        pass