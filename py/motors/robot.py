import logging
from time import sleep

from gpiozero import Motor, Robot

from py.exchange_data import ExchangeData
from py.multiprocessor import MultiProcessor

log = logging.getLogger(__name__)


class RobotController(MultiProcessor.Runner):
    def __init__(self, shared_data: ExchangeData):
        self.__data: ExchangeData = shared_data
        self.__robot = Robot(left=Motor(27, 22), right=Motor(6, 5))

    def run(self) -> None:
        log.info("Robot started!")

        try:
            while True:
                match self.__data.key_pressed:
                    case 'k':
                        self.__move(self.__robot.forward, 'forward')
                    case 'j':
                        self.__move(self.__robot.backward, 'backward')
                    case 'h':
                        self.__move(self.__robot.left, 'left')
                    case 'l':
                        self.__move(self.__robot.right, 'right')
        except Exception as e:
            log.warning(f"Interrupted: {e}!")

        log.info("Robot stopped!")

    def __move(self, move: lambda: [[], None], name: str, delay: float = 0.1) -> None:
        log.info(f'{name}-{delay}s,stop')

        move()
        sleep(delay)
        self.__robot.stop()
