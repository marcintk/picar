import multiprocessing
import os
from collections.abc import Callable
from multiprocessing import Process


class MultiProcessorRunner(object):
    def run(self) -> None:
        raise Exception('not implemented!')


class _Wrapper(object):
    def __init__(self, runner: Callable[[], MultiProcessorRunner]) -> None:
        self.runner: Callable[[], MultiProcessorRunner] = runner

    def target(self):
        self.runner().run()


class MultiProcessor(object):
    def __init__(self) -> None:
        self.processes: [Process] = []

    def add(self, runner: Callable[[], MultiProcessorRunner]) -> 'MultiProcessor':
        self.processes.append(multiprocessing.Process(target=_Wrapper(runner).target))
        return self

    def start(self) -> 'MultiProcessor':
        # printing main program process id
        print("Main process id: {}".format(os.getpid()))

        # starting processes
        for process in self.processes:
            process.start()
            print("Sub-process started: {}".format(process.pid))

        return self

    def join(self) -> None:
        # wait until processes are finished
        for process in self.processes:
            print("Waiting on process: {}".format(process.pid))
            process.join()

        # all processes finished
        print("All processes finished execution!")
