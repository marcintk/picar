import multiprocessing
import os
import time

from py.aikit.detection import GStreamerDetectionApp, user_app_callback_class
from py.aikit.hailo_rpi_common import get_default_parser
from py.sensehat.sense import SenseDisplay

user_data = user_app_callback_class()
sense = SenseDisplay()

def worker1():
    parser = get_default_parser()
    # Add additional arguments here
    parser.add_argument(
        "--network",
        default="yolov6n",
        choices=['yolov6n', 'yolov8s', 'yolox_s_leaky'],
        help="Which Network to use, default is yolov6n",
    )
    parser.add_argument(
        "--hef-path",
        default=None,
        help="Path to HEF file",
    )
    parser.add_argument(
        "--labels-json",
        default=None,
        help="Path to costume labels JSON file",
    )
    args = parser.parse_args()
    app = GStreamerDetectionApp(args, user_data)
    app.run()

def worker2():
    while True:
        print("Worker2", user_data.detected.value)

        if user_data.detected.value > 0:
            sense.show(user_data.detected.value)
        else:
            sense.clear()

        time.sleep(0.1)


if __name__ == "__main__":
    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))

    # creating processes
    p1 = multiprocessing.Process(target=worker1)
    p2 = multiprocessing.Process(target=worker2)

    # starting processes
    p1.start()
    p2.start()

    # process IDs
    print("ID of process p1: {}".format(p1.pid))
    print("ID of process p2: {}".format(p2.pid))

    # wait until processes are finished
    p2.join()
    print("P2 process finished execution!")

    p1.join()
    print("P1 process finished execution!")

    # both processes finished
    print("Both processes finished execution!")

    # check if processes are alive
    print("Process p1 is alive: {}".format(p1.is_alive()))
    print("Process p2 is alive: {}".format(p2.is_alive()))
