# GPIO fix for Raspi5:
# https://github.com/gpiozero/gpiozero/issues/1166

import gpiozero.pins.lgpio
import lgpio


def __patched_init(self, chip=None):
    gpiozero.pins.lgpio.LGPIOFactory.__bases__[0].__init__(self)
    chip = 0
    self._handle = lgpio.gpiochip_open(chip)
    self._chip = chip
    self.pin_class = gpiozero.pins.lgpio.LGPIOPin


gpiozero.pins.lgpio.LGPIOFactory.__init__ = __patched_init
