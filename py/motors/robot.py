from time import sleep

from gpiozero import Motor, Robot

class RobotControl(object):
    def __init__(self):
        left = Motor(27, 22)
        right = Motor(5, 6)
        self._robot = Robot(left=left, right=right)

    def forward(self):
        print('forward')
        self._robot.forward()

    def backward(self):
        print('backward')
        self._robot.backward()

    def left(self):
        print('left')
        self._robot.left()

    def right(self):
        print('right')
        self._robot.right()

    def stop(self):
        print('stop')
        self._robot.stop()

if __name__ == "__main__":
    control = RobotControl()
    control.forward()
    sleep(1)
    control.backward()
    sleep(1)
    control.left()
    sleep(1)
    control.right()
    sleep(1)
    control.stop()