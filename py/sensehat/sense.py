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
        self.__last_display: int = 0

    def run(self) -> None:
        log.info("SenseDisplay started!")

        try:
            self.__sense.set_rotation(270)

            while True:
                new_display = self.__exchange_data.persons_detected

                if self.__last_display != new_display:
                    self.__last_display = new_display
                    self.__sense.show_letter(str(new_display), text_colour=_RED)

                    log.info("SenseDisplay: display=%d", new_display)

                time.sleep(0.1)
        except Exception as e:
            log.warning(f"Interrupted: {e}!")
        finally:
            self.__sense.clear()

        log.info("SenseDisplay stopped!")
