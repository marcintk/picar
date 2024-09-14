import time

from sense_hat import SenseHat

from py.multiprocessor import MultiProcessorRunner
from py.shared_data import SharedData

_RED = (255, 0, 0)


class SenseDisplay(MultiProcessorRunner):
    def __init__(self, shared_data: SharedData):
        self.shared_data: SharedData = shared_data
        self.sense: SenseHat = SenseHat()

        self.sense.set_rotation(180)

    def show(self, digit: int):
        self.sense.show_letter(str(digit), text_colour=_RED)

    def clear(self):
        self.sense.clear()

    def run(self) -> None:
        print("SenseDisplay started!")

        while True:
            print("SenseDisplay: detected=", self.shared_data.detected.value)

            if self.shared_data.detected.value > 0:
                self.show(self.shared_data.detected.value)
            else:
                self.sense.clear()

            time.sleep(0.1)
