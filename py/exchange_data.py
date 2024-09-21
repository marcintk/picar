# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
import multiprocessing

from py.aikit.api.streamer import HailoGStreamer


class ExchangeData(HailoGStreamer.Data):
    def __init__(self):
        super().__init__()
        self.person_detected = multiprocessing.Value('i', 0)
