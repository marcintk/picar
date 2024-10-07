import logging
from time import sleep

from gpiozero import Motor, Robot

from py.data import RobotData, Keystroke
from py.multiprocessor import MultiProcessor

log = logging.getLogger(__name__)


class RobotController(MultiProcessor.Runner):
    def __init__(self, shared_data: RobotData):
        self.__data: RobotData = shared_data
        self.__robot = Robot(left=Motor(27, 22), right=Motor(6, 5))

    def run(self) -> None:
        log.info("Robot started!")

        try:
            while True:
                match self.__data.key_pressed:
                    case Keystroke.FORWARD:
                        self.__move(self.__robot.forward, 'move forward')
                    case Keystroke.BACKWARD:
                        self.__move(self.__robot.backward, 'move backward')
                    case Keystroke.LEFT:
                        self.__move(self.__robot.left, 'turn left')
                    case Keystroke.RIGHT:
                        self.__move(self.__robot.right, 'turn right')
        except Exception as e:
            log.warning(f"Interrupted: {e}!")
        finally:
            self.__robot.stop()

        log.info("Robot stopped!")

    def __move(self, move: lambda: [[], None], display: str, delay: float = 0.1) -> None:
        log.info(f'{display} [{delay}s]')

        move()
        sleep(delay)
        self.__robot.stop()
