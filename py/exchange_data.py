# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# Inheritance from the app_callback_class
import multiprocessing
from enum import Enum

from readchar import key

from py.aikit.api.streamer import HailoGStreamer


class Keystroke(Enum):
    NONE = 0, []
    LEFT = 1, ['h', key.LEFT]
    RIGHT = 2, ['l', key.RIGHT]
    FORWARD = 3, ['k', key.UP]
    BACKWARD = 4, ['j', key.DOWN]

    def code(self) -> int:
        return self.value[0]

    def __keystrokes(self) -> list[str]:
        return self.value[1]

    @staticmethod
    def from_int(code: int) -> 'Keystroke':
        for enum in Keystroke:
            if enum.code() == code:
                return enum
        return Keystroke.NONE

    @staticmethod
    def from_str(keystroke: str) -> 'Keystroke':
        for enum in Keystroke:
            if keystroke in enum.__keystrokes():
                return enum
        return Keystroke.NONE


class ExchangeData(HailoGStreamer.Data):
    def __init__(self):
        super().__init__()

        self.__persons_detected = multiprocessing.Value('i', 0)
        self.__key_pressed = multiprocessing.Value('i', 0)

    #
    # Persons detected
    #

    @property
    def persons_detected(self) -> int:
        return self.__persons_detected.value

    def new_persons_detected(self, count: int):
        self.__update_variable(self.__persons_detected, count)

    #
    # Key Pressed
    #

    @property
    def key_pressed(self) -> Keystroke:
        value: int = self.__key_pressed.value
        self.reset_key_pressed()
        return Keystroke.from_int(value)

    def reset_key_pressed(self):
        self.new_key_pressed()

    def new_key_pressed(self, keystroke: str = ''):
        self.__update_variable(self.__key_pressed, Keystroke.from_str(keystroke).code())

    #
    # Internals
    #

    @staticmethod
    def __update_variable(variable: multiprocessing.Value, value: int):
        variable.acquire()
        variable.value = value
        variable.release()
