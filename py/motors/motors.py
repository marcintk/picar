import logging
from time import sleep
from typing import Callable

from gpiozero import Motor, Robot

from py.data import RobotData, Keystroke
from py.multiprocessor import MultiProcessor

log = logging.getLogger(__name__)


class MotorsController(MultiProcessor.Runner):
    def __init__(self, shared_data: RobotData):
        self.__data: RobotData = shared_data
        self.__robot = Robot(left=Motor(27, 22), right=Motor(6, 5))

    def run(self) -> None:
        log.info("Motors started!")

        try:
            while True:
                match self.__data.key_pressed:
                    case Keystroke.FORWARD:
                        self.__move(self.__robot.forward, display='move forward', delay=0.1)
                    case Keystroke.BACKWARD:
                        self.__move(self.__robot.backward, display='move backward', delay=0.1)
                    case Keystroke.LEFT:
                        self.__move(self.__robot.left, display='turn left')
                    case Keystroke.RIGHT:
                        self.__move(self.__robot.right, display='turn right')
                    case _:
                        sleep(0.1)
        except Exception as e:
            log.warning(f"Interrupted: {e}!")
        finally:
            self.__robot.stop()

        log.info("Motors stopped!")

    def __move(self, move: Callable[[], None], *, display: str, delay: float = 0.025) -> None:
        log.info(f'{display} [{delay}s]')

        move()
        sleep(delay)
        self.__robot.stop()
