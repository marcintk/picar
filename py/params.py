_bools = ('NO', 'YES')


class Parameters(object):
    def __init__(self, network: str, video_input: str, show_display: bool, skip_detection: bool, plot_detection: bool, show_fps: bool, verbose: bool):
        self.network: str = network
        self.video_input: str = video_input
        self.show_display: bool = show_display
        self.skip_detection: bool = skip_detection
        self.plot_detection: bool = plot_detection
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

    def __str__(self):
        return 'PARAMS:\n  ' + '\n  '.join(['---',  #
                                            f'network: {self.network}',  #
                                            f'video_input: {self.video_input}',  #
                                            f'show_display: {_bools[self.show_display]}',  #
                                            f'skip_detection: {_bools[self.skip_detection]}',  #
                                            f'plot_detection: {_bools[self.plot_detection]}',  #
                                            f'show_fps: {_bools[self.show_fps]}',  #
                                            f'verbose: {_bools[self.verbose]}',  #
                                            '---'])
