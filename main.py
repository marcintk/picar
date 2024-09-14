import logging

from py.aikit.detection import GStreamerDetectionApp
from py.aikit.hailo_rpi_common import GStreamerSharedData
from py.argparse import ArgsParser
from py.multiprocessor import MultiProcessor, MultiProcessorRunner
from py.params import Parameters
from py.sensehat.sense import SenseDisplay
from py.shared_data import SharedData

log = logging.getLogger(__name__)


class GStreamerWrapper(MultiProcessorRunner):
    def __init__(self, params: Parameters, shared_data: GStreamerSharedData):
        self.params = params
        self.shared_data = shared_data

    def run(self) -> None:
        GStreamerDetectionApp(self.params, self.shared_data).run()


def main():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s | %(name)-10s] %(message)s')

    try:
        params: Parameters = ArgsParser().parse()
        log.info(params)

        if params.verbose:
            log.setLevel(logging.DEBUG)

        shared_data = SharedData()

        processor = MultiProcessor()
        processor.add(SenseDisplay(shared_data))
        processor.add(GStreamerWrapper(params, shared_data))
        processor.start()
        processor.join()

    except KeyboardInterrupt:
        log.error("Keyboard Interrupt!")
    except KeyError as e:
        log.error(f'ERROR: {e}')
    except ValueError as e:
        log.error(f'ERROR: {e}')


if __name__ == "__main__":
    main()
