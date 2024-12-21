from enum import Enum

_bools = ('NO', 'YES')


class Parameters(object):
    class DisplayType(Enum):
        DEFAULT = 0
        NO_DISPLAY = 1
        TCP_SINK = 2

        def is_fake(self) -> bool:
            return self == Parameters.DisplayType.NO_DISPLAY

        def is_tcp_sink(self) -> bool:
            return self == Parameters.DisplayType.TCP_SINK

        def __str__(self) -> str:
            return self.name

        def __repr__(self) -> str:
            return self.name

        @staticmethod
        def from_string(s: str) -> 'Parameters.DisplayType':
            try:
                return Parameters.DisplayType[s]
            except KeyError:
                raise ValueError()

    def __init__(self, network: str, video_input: str, display: DisplayType, skip_detection: bool, show_fps: bool, verbose: bool):
        self.network: str = network
        self.video_input: str = video_input
        self.display: Parameters.DisplayType = display
        self.skip_detection: bool = skip_detection
        self.show_fps: bool = show_fps
        self.verbose: bool = verbose

    def get_source_type(self) -> str:
        if self.video_input.startswith("/dev/video"):
            return 'usb'
        else:
            if self.video_input.startswith("rpi"):
                return 'rpi'
            else:
                return 'file'

    def __str__(self) -> str:
        return 'PARAMS:\n  ' + '\n  '.join(['---',  #
                                            f'network: {self.network}',  #
                                            f'video_input: {self.video_input}',  #
                                            f'display: {self.display}',  #
                                            f'skip_detection: {_bools[self.skip_detection]}',  #
                                            f'show_fps: {_bools[self.show_fps]}',  #
                                            f'verbose: {_bools[self.verbose]}',  #
                                            '---'])
