import argparse

from py.params import Parameters


class ArgsParser(object):
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=120))
        self._parser.add_argument("-vi", "--input", help="video input: mp4, mpg, rpi, rtsp", metavar="<name>", required=True)
        self._parser.add_argument("-n", "--network", help="network type: [yolov6n/yolov8s/yolov8s_pose]", type=str, default='yolov8s')
        self._parser.add_argument("-d",
                                  "--display",
                                  help="display type",
                                  type=Parameters.DisplayType.from_string,
                                  choices=list(Parameters.DisplayType),
                                  default=Parameters.DisplayType.DEFAULT)
        self._parser.add_argument("-sd", "--skip-detection", help="disallow AI detector", action="store_true")
        self._parser.add_argument("-sf", "--show-fps", help="Print FPS on sink", action="store_true")
        self._parser.add_argument("-v", "--verbose", help="change log level to DEBUG", action="store_true")

    def parse(self) -> Parameters:
        args = self._parser.parse_args()

        return Parameters(network=args.network,
                          video_input=args.input,
                          display=args.display,
                          skip_detection=args.skip_detection,
                          show_fps=args.show_fps,
                          verbose=args.verbose)
