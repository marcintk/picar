import logging
import multiprocessing
import os
from collections.abc import Callable
from multiprocessing import Process

from readchar import readkey

from py.data import RobotData

log = logging.getLogger(__name__)


class MultiProcessor(object):
    class Runner(object):
        def run(self) -> None:
            raise Exception('not implemented!')

    class __Wrapper(object):
        def __init__(self, runner: Callable[[], 'MultiProcessor.Runner']) -> None:
            self.runner: Callable[[], MultiProcessor.Runner] = runner

        def target(self):
            self.runner().run()

    def __init__(self, data: RobotData) -> None:
        self.data: RobotData = data
        self.processes: [Process] = []

        log.info(f'Multiprocessor with {os.cpu_count()} CPUs available.')

    def add(self, runner: Callable[[], Runner], enable: bool = True) -> 'MultiProcessor':
        if enable:
            self.processes.append(multiprocessing.Process(target=MultiProcessor.__Wrapper(runner).target))
        return self

    def start(self) -> 'MultiProcessor':
        # printing main program process id
        log.info("Main process id: {}".format(os.getpid()))

        # starting processes
        for process in self.processes:
            process.start()
            log.info("Sub-process started: {}".format(process.pid))

        return self

    def join(self) -> None:
        # wait until processes are finished
        for process in self.processes:
            log.info("Waiting on process: {}".format(process.pid))
            process.join()

        # all processes finished
        log.info("All processes finished execution!")

    def keyboard(self):
        while True:
            key: str = readkey()
            self.data.new_key_pressed(key)

            if key == 'q':
                raise KeyboardInterrupt('User Exit')

    def terminate(self) -> None:
        for process in self.processes:
            process.terminate()
            log.info("Sub-process terminated: {}".format(process.pid))
