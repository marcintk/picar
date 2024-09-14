import time

from sense_hat import SenseHat

from main import PicarSharedData
from py.multiprocessor import MultiProcessorRunner

_RED = (255, 0, 0)


class SenseDisplay(MultiProcessorRunner):
    def __init__(self, shared_data: PicarSharedData):
        self.shared_data: PicarSharedData = shared_data
        self.sense: SenseHat = SenseHat()

        self.sense.set_rotation(180)

    def show(self, digit: int):
        self.sense.show_letter(str(digit), text_colour=_RED)

    def clear(self):
        self.sense.clear()

    def run(self):
        while True:
            print("Worker2", self.shared_data.detected.value)

            if self.shared_data.detected.value > 0:
                self.sense.show(self.shared_data.detected.value)
            else:
                self.sense.clear()

            time.sleep(0.1)
