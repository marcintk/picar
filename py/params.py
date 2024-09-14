import os

_bools = ('NO', 'YES')


class Parameters(object):
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

    def __init__(self, network: str, video_input: str, show_display: bool, skip_detection: bool, plot_detection: bool, show_fps: bool, verbose: bool):
        self.network: str = network
        self.video_input: str = video_input
        self.show_display: bool = show_display
        self.skip_detection: bool = skip_detection
        self.plot_detection: bool = plot_detection
        self.show_fps: bool = show_fps
        self.verbose: bool = verbose

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
