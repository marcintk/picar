import logging

from py.aikit.ai_person_detection import AiPersonDetector
from py.argparse import ArgsParser
from py.exchange_data import ExchangeData
from py.motors.robot import RobotController
from py.multiprocessor import MultiProcessor
from py.params import Parameters
from py.sensehat.sense import SenseDisplay

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s | %(name)-10s] - %(message)s')

    try:
        params: Parameters = ArgsParser().parse()
        log.info(params)

        if params.verbose:
            log.setLevel(logging.DEBUG)

        data = ExchangeData()
        processor = MultiProcessor()
        processor.add(lambda: SenseDisplay(data))
        processor.add(lambda: RobotController(data))
        processor.add(lambda: AiPersonDetector(params, data))
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
