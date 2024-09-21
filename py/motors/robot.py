import logging
from time import sleep

from gpiozero import Motor, Robot

from py.exchange_data import ExchangeData
from py.multiprocessor import MultiProcessor

log = logging.getLogger(__name__)


class RobotController(MultiProcessor.Runner):
    def __init__(self, shared_data: ExchangeData):
        self.__exchange_data: ExchangeData = shared_data
        self.__robot = Robot(left=Motor(27, 22), right=Motor(6, 5))

    def run(self) -> None:
        log.info("Robot started!")

        while True:
            if self.__exchange_data.person_detected.value > 0:
                self.turn_left()
                sleep(0.1)
                self.stop()

            sleep(5)

    def move_forward(self):
        print('forward')
        self.__robot.forward()

    def move_backward(self):
        print('backward')
        self.__robot.backward()

    def turn_left(self):
        print('left')
        self.__robot.left()

    def turn_right(self):
        print('right')
        self.__robot.right()

    def stop(self):
        print('stop')
        self.__robot.stop()
