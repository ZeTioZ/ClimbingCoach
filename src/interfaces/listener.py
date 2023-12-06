from abc import ABC, abstractmethod

from enums.event_type import EventType
from interfaces.event import Event


class Listener(ABC):
	def __init__(self, event_types) -> None:
		super().__init__()
		self.listened_event_types: EventType = event_types

	@abstractmethod
	def update(self, event: Event, update_event_types: [EventType], *args, **kwargs):
		pass
