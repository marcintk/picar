# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
import multiprocessing

from py.aikit.hailo_rpi_common import GStreamerCallbackClass


class SharedData(GStreamerCallbackClass):
    def __init__(self):
        super().__init__()
        self.detected = multiprocessing.Value('i', 0)
