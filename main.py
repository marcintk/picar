import logging

from py.argparse import ArgsParser
from py.params import Parameters
from py.multiprocessor import MultiProcessor

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s | %(name)-10s] %(message)s')

    try:
        params: Parameters = ArgsParser().parse()
        log.info(params)

        if params.verbose:
            log.setLevel(logging.DEBUG)

        processor=MultiProcessor(params)
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
