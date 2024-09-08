import os
from enum import Enum

_bools = ('NO', 'YES')


class Parameters(object):
    class DetectorType(Enum):
        NONE = 0
        HAAR = 1
        YOLO = 2

        def __str__(self):
            return self.name

        def __repr__(self):
            return self.name

        @staticmethod
        def from_string(s):
            try:
                return Parameters.DetectorType[s]
            except KeyError:
                raise ValueError()

    class ComputeUnit(Enum):
        CPU = "cpu"
        CUDA = "cuda"
        MKL = "mkl"
        MPS = "mps"
        OPENMP = "openmp"

        def __str__(self):
            return self.value

        def __repr__(self):
            return self.value

        @staticmethod
        def from_string(s):
            try:
                return Parameters.ComputeUnit[s.upper()]
            except KeyError:
                raise ValueError(f'Invalid compute unit: {s}')

    class Input(object):
        def __init__(self, video_input: str, rtsp_input: bool, device_input: str, device_backend: str, device_resolution: (int, int)):
            self.video_input: str = video_input
            self.rtsp_input: bool = rtsp_input
            self.device_input: str = device_input
            self.device_backend: str = device_backend
            self.device_resolution: (int, int) = device_resolution
            self.rtsp_url = self._load_rtsp_url()

        def rtsp_ip(self):
            return self.rtsp_url.split("@")[1]

        def __str__(self):
            return '\n  '.join([f'video_input: {self.video_input}',  #
                                f'rtsp_input: {_bools[self.rtsp_input]}',  #
                                f'rtsp_url: {self.rtsp_ip()}',  #
                                f'device_input: {self.device_input}',  #
                                f'device_backend: {self.device_backend}',  #
                                f'device_resolution: {self.device_resolution}'])

        @staticmethod
        def _load_rtsp_url() -> str:
            url = os.getenv("CAMERA_URL")
            user = os.getenv("CAMERA_USER")
            password = os.getenv("CAMERA_PASSWORD")
            return f"rtsp://{user}:{password}@{url}"

    def __init__(self,
                 detector_type: DetectorType,
                 detector_model: str,
                 detector_confidence: float,
                 detector_max_objects: int,
                 compute_unit: ComputeUnit,
                 frame_probing: int,
                 frame_resize: (int, int),
                 show_display: bool,
                 plot_detection: bool,
                 video_input: str,
                 rtsp_input: bool,
                 device_input: str,
                 device_backend: str,
                 device_resolution: (int, int),
                 verbose: bool):
        self.detector_type: Parameters.DetectorType = detector_type
        self.detector_model: str = detector_model
        self.detector_confidence = detector_confidence
        self.detector_max_objects = detector_max_objects
        self.compute_unit: Parameters.ComputeUnit = compute_unit
        self.frame_probing: int = frame_probing
        self.frame_resize: (int, int) = frame_resize
        self.show_display: bool = show_display
        self.plot_detection: bool = plot_detection
        self.verbose: bool = verbose
        self.input: Parameters.Input = Parameters.Input(video_input, rtsp_input, device_input, device_backend, device_resolution)

    def resize(self):
        return self.frame_resize is not None

    def __str__(self):
        return 'PARAMS:\n  ' + '\n  '.join(['---',  #
                                            f'detector: {self.detector_type}',  #
                                            f'model: {self.detector_model}',  #
                                            f'confidence: {self.detector_confidence}',  #
                                            f'max_objects: {self.detector_max_objects}',  #
                                            f'compute_unit: {self.compute_unit}',  #
                                            f'frame_probing: {self.frame_probing}',  #
                                            f'frame_resize: {self.frame_resize}',  #
                                            f'show_display: {_bools[self.show_display]}',  #
                                            f'draw_detection: {_bools[self.plot_detection]}',  #
                                            f'{self.input}',  #
                                            f'verbose: {_bools[self.verbose]}',  #
                                            '---'])
