import multiprocessing
import os
import time

from py.aikit.detection import GStreamerDetectionApp, user_app_callback_class
from py.params import Parameters
from py.sensehat.sense import SenseDisplay


class MultiProcessor(object):
    def __init__(self, params: Parameters):
        self.params: Parameters = params
        self.user_data = user_app_callback_class()
        self.sense = SenseDisplay()

        # creating processes
        self.p1 = multiprocessing.Process(target=self.__worker1)
        self.p2 = multiprocessing.Process(target=self.__worker2)

    def start(self):
        # printing main program process id
        print("ID of main process: {}".format(os.getpid()))

        # starting processes
        self.p1.start()
        self.p2.start()

        # process IDs
        print("ID of process p1: {}".format(self.p1.pid))
        print("ID of process p2: {}".format(self.p2.pid))

    def join(self):
        # wait until processes are finished
        self.p2.join()
        print("P2 process finished execution!")

        self.p1.join()
        print("P1 process finished execution!")

        # both processes finished
        print("Both processes finished execution!")

        # check if processes are alive
        print("Process p1 is alive: {}".format(self.p1.is_alive()))
        print("Process p2 is alive: {}".format(self.p2.is_alive()))

    def __worker1(self):
        app = GStreamerDetectionApp(self.params, self.user_data)
        app.run()

    def __worker2(self):
        while True:
            print("Worker2", self.user_data.detected.value)

            if self.user_data.detected.value > 0:
                self.sense.show(self.user_data.detected.value)
            else:
                self.sense.clear()

            time.sleep(0.1)
