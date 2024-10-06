# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
import multiprocessing

from py.aikit.api.streamer import HailoGStreamer


class ExchangeData(HailoGStreamer.Data):
    def __init__(self):
        super().__init__()

        self.__persons_detected = multiprocessing.Value('i', 0)
        self.__key_pressed = multiprocessing.Value('i', 0)

    @property
    def persons_detected(self) -> int:
        return self.__persons_detected.value

    @property
    def key_pressed(self) -> str:
        value: int = self.__key_pressed.value
        self.reset_key_pressed()
        return chr(value)

    def new_persons_detected(self, count: int):
        self.__persons_detected.acquire()
        self.__persons_detected.value = count
        self.__persons_detected.release()

    def reset_key_pressed(self):
        self.new_key_pressed('0')

    def new_key_pressed(self, key: str):
        self.__key_pressed.acquire()
        self.__key_pressed.value = ord(key[0])
        self.__key_pressed.release()
