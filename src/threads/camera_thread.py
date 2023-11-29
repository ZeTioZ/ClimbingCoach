from threading import Thread

from events.flux_reader_event import FluxReaderEvent


class Camera(Thread):
	def __init__(self, flux: int | str = 0, nbr_frame_to_skip: int = 2):
		super().__init__()
		self.daemon = True
		self.flux_reader_event = FluxReaderEvent(flux, nbr_frame_to_skip)

	def run(self):
		self.flux_reader_event.process()

	def stop(self):
		self.flux_reader_event.set_cancelled(True)
