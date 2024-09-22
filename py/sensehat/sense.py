import logging
import time

from sense_hat import SenseHat

from py.exchange_data import ExchangeData
from py.multiprocessor import MultiProcessor

_RED = (255, 0, 0)

log = logging.getLogger(__name__)


class SenseDisplay(MultiProcessor.Runner):
    def __init__(self, exchange_data: ExchangeData):
        self.__exchange_data: ExchangeData = exchange_data
        self.__sense: SenseHat = SenseHat()

        self.__sense.set_rotation(180)

    def show(self, digit: int):
        self.__sense.show_letter(str(digit), text_colour=_RED)

    def clear(self):
        self.__sense.clear()

    def run(self) -> None:
        log.info("SenseDisplay started!")

        while True:
            log.debug("SenseDisplay: detected=%d", self.__exchange_data.person_detected.value)

            if self.__exchange_data.person_detected.value > 0:
                self.show(self.__exchange_data.person_detected.value)
            else:
                self.__sense.clear()

            time.sleep(0.1)
