from events.flux_reader_event import FluxReaderEvent
from threading import Thread

class Camera(Thread):
    def __init__(self, flux: str = "0", width: int = 640, height: int = 480, nbr_frame_to_skip: int = 2):
        Thread.__init__(self)
        self.daemon = True
        self.flux_reader_event = FluxReaderEvent(flux, width, height, nbr_frame_to_skip)
    

    def run(self):
        self.flux_reader_event.process()


    def stop(self):
        self.flux_reader_event.set_cancelled(True)
