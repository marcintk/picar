import logging

from py.aikit.aidetector import AiDetector
from py.argparse import ArgsParser
from py.data import RobotData
from py.motors.robot import RobotController
from py.multiprocessor import MultiProcessor
from py.params import Parameters
from py.sensehat.sense import SenseDisplay

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s | %(name)-10s] - %(message)s')

    data = RobotData()
    processor = MultiProcessor(data)

    try:
        params: Parameters = ArgsParser().parse()
        log.info(params)

        if params.verbose:
            logging.root.setLevel(logging.DEBUG)

        processor.add(lambda: SenseDisplay(data))
        processor.add(lambda: RobotController(data))
        processor.add(lambda: AiDetector(params, data), enable=not params.skip_detection)
        processor.start()
        processor.keyboard()

    except KeyboardInterrupt as e:
        log.error(f'Keyboard Interrupt: {e}!')
    except KeyError as e:
        log.error(f'ERROR: {e}')
    except ValueError as e:
        log.error(f'ERROR: {e}')
    finally:
        processor.terminate()


if __name__ == "__main__":
    main()
