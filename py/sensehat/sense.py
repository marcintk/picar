from time import sleep

from sense_hat import SenseHat

_RED = (255, 0, 0)


class SenseDisplay(object):
    def __init__(self):
        self.sense = SenseHat()
        self.sense.set_rotation(180)

    def show(self, digit: int):
        self.sense.show_letter(str(digit), text_colour=_RED)

    def clear(self):
        self.sense.clear()


if __name__ == "__main__":
    display = SenseDisplay()
    display.show()
    sleep(1)
    display.clear()
