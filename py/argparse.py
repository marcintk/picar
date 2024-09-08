import argparse

from py.params import Parameters


class ArgsParser(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=120))
        self._parser.add_argument("-d",
                                  "--detector",
                                  help="detector type: [NONE/YOLO/HAAR]",
                                  type=Parameters.DetectorType.from_string,
                                  choices=list(Parameters.DetectorType),
                                  default=Parameters.DetectorType.YOLO)
        self._parser.add_argument("-cu",
                                  "--compute-unit",
                                  help="compute unit",
                                  type=Parameters.ComputeUnit.from_string,
                                  choices=list(Parameters.ComputeUnit),
                                  default=Parameters.ComputeUnit.CPU)
        self._parser.add_argument("-m", "--model", help="model name, default=yolov8m.pt", metavar="<name>", type=str, required=False, default='yolov8m.pt')
        self._parser.add_argument("--confidence", help="detector confidence threshold, default=0.5", metavar="<value>", type=float, required=False, default=0.5)
        self._parser.add_argument("--max-objects",
                                  help="maximum number of detections per image: default=300",
                                  metavar="<value>",
                                  type=int,
                                  required=False,
                                  default=300)
        self._parser.add_argument("-fp", "--probing", help="frame probing: default=10", metavar="<value>", type=int, required=False, default=1)
        self._parser.add_argument("-fr", "--resize", help="frame resize: i.e. 640 480", metavar=('<width>', '<height>'), type=int, nargs=2, required=False)
        self._parser.add_argument("-nd", "--no-detection", help="do not detect (same as detector=NONE)", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-nv", "--no-view", help="do not display a view output", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-np", "--no-plotting", help="do not plot detected objects", action=argparse.BooleanOptionalAction, default=False)
        self._parser.add_argument("-vi", "--video-input", help="video input: mp4, mpg", metavar="<file>", required=False)
        self._parser.add_argument("-rtsp",
                                  "--rtsp-input",
                                  help="use rtsp protocol as an input (settings in .env)",
                                  action=argparse.BooleanOptionalAction,
                                  default=False)
        self._parser.add_argument("-di", "--device-input", help="device index: 0, 1", metavar="<index>", required=False, default=0)
        self._parser.add_argument("-db", "--device-backend", help="device backend: GSTREAMER, V4L2", metavar="<name>", required=False, default=None)
        self._parser.add_argument("-dr", "--device-resolution", help="device resolution", metavar=('<width>', '<height>'), type=int, nargs=2, required=False)
        self._parser.add_argument("-v", "--verbose", help="increase output verbosity", action=argparse.BooleanOptionalAction, default=False)

    def parse(self) -> Parameters:
        args = self._parser.parse_args()
        parameters = Parameters(detector_type=Parameters.DetectorType.NONE if args.no_detection else args.detector,
                                detector_model=args.model,
                                detector_confidence=args.confidence,
                                detector_max_objects=args.max_objects,
                                compute_unit=args.compute_unit,
                                frame_probing=args.probing,
                                frame_resize=args.resize,
                                show_display=not args.no_view,
                                plot_detection=not args.no_plotting,
                                video_input=args.video_input,
                                rtsp_input=args.rtsp_input,
                                device_input=args.device_input,
                                device_backend=args.device_backend,
                                device_resolution=args.device_resolution,
                                verbose=args.verbose)

        return parameters
