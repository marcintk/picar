from time import sleep

from sense_hat import SenseHat

_RED = (255, 0, 0)

class SenseDisplay(object):
    def __init__(self):
        self.sense = SenseHat()
        self.sense.set_rotation(180)
        self.shows = False


    def show(self):
        if not self.shows:
            self.sense.show_letter("X", text_colour=_RED)
            self.shows = True

    def clear(self):
        if self.shows:
            self.sense.clear()
            self.shows = False


if __name__ == "__main__":
    display = SenseDisplay()
    display.show()
    sleep(1)
    display.clear()
