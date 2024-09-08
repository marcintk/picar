from time import sleep

from gpiozero import Motor


class MotorControl(object):
    def __init__(self):
        self._motor = Motor(6, 5)

    def forward(self):
        print('forward')
        self._motor.forward()

    def backward(self):
        print('backward')
        self._motor.backward()

    def stop(self):
        print('stop')
        self._motor.stop()

if __name__ == "__main__":
    control = MotorControl()
    control.forward()
    sleep(1)
    control.backward()
    sleep(1)
    control.stop()
