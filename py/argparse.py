import argparse

from py.params import Parameters


class ArgsParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=120))
        self._parser.add_argument("-n", "--network", help="network type: [yolov6n/yolov8s_h8l]", type=str, default='yolov8s_h8l]')
        self._parser.add_argument("-nv", "--no-view", help="do not display a view output", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-nd", "--no-detection", help="do not detect (same as detector=NONE)", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-np", "--no-plotting", help="do not plot detected objects", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-f", "--show-fps", action="store_true", help="Print FPS on sink")
        self._parser.add_argument("-vi", "--input", help="video input: mp4, mpg, rpi, rtsp", metavar="<name>", required=True)
        self._parser.add_argument("-v", "--verbose", help="increase output verbosity", action=argparse.BooleanOptionalAction, default=False)

    def parse(self) -> Parameters:
        args = self._parser.parse_args()
        parameters = Parameters(network=args.network,
                                video_input=args.input,
                                show_display=not args.no_view,
                                skip_detection=args.no_detection,
                                plot_detection=not args.no_plotting,
                                show_fps=args.show_fps,
                                verbose=args.verbose)

        return parameters
