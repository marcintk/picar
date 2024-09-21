RESOURCES = './py/aikit/api/resources/'


def QUEUE(name, max_size_buffers: int = 3, max_size_bytes: int = 0, max_size_time: int = 0, leaky: str = 'no') -> str:
    return f"queue name={name} leaky={leaky} max-size-buffers={max_size_buffers} max-size-bytes={max_size_bytes} max-size-time={max_size_time} ! "


def VIDEO_RAW(framerate: str = '', format: str = '', width: int | None = None, height: int | None = None, pixel_aspect_ratio: str = '') -> str:
    has_caps = len(format) > 0 or width is not None or height is not None or len(pixel_aspect_ratio) > 0

    return "{}{}{}{}{}{}{}".format('video/x-raw' if has_caps else '',
                                   f', framerate={framerate}' if len(framerate) > 0 else '',
                                   f', format={format}' if len(format) > 0 else '',
                                   f', width={width}' if width is not None else '',
                                   f', height={height}' if height is not None else '',
                                   f', pixel-aspect-ratio={pixel_aspect_ratio}' if len(pixel_aspect_ratio) > 0 else '',
                                   ' ! ' if has_caps else '')


def VIDEO_SCALE(threads: int = 1, framerate: str = '', format: str = '', width: int | None = None, height: int | None = None) -> str:
    return "videoscale{} ! {}".format(f' n-threads={threads}' if threads > 1 else '',
                                      VIDEO_RAW(framerate=framerate, format=format, width=width, height=height))


def VIDEO_CONVERT(threads: int = 3,
                  name: str = '',
                  qos: str = '',
                  format: str = '',
                  width: int | None = None,
                  height: int | None = None,
                  pixel_aspect_ratio: str = '') -> str:
    return "videoconvert{}{}{} ! {}".format(f' n-threads={threads}',
                                            f' name={name}' if len(name) > 0 else '',
                                            f' qos={qos}' if len(qos) > 0 else '',
                                            VIDEO_RAW(format=format, width=width, height=height, pixel_aspect_ratio=pixel_aspect_ratio))


def TEE(variable: str) -> str:
    return f"tee name={variable} ! "


def FPS_DISPLAY_SINK(video_sink: str, sync: str, show_fps: bool) -> str:
    return f"fpsdisplaysink video-sink={video_sink} name=hailo_display sync={sync} text-overlay={show_fps} signal-fps-measurements=true"


def HAILO_NET(hef_path: str, batch_size: int, nms_score: float, nms_iou: float) -> str:
    return (f"hailonet hef-path={hef_path} batch-size={batch_size} nms-score-threshold={nms_score} nms-iou-threshold={nms_iou} "
            f"output-format-type=HAILO_FORMAT_TYPE_FLOAT32 force-writable=true ! ")


def HAILO_FILTER(labels: str) -> str:
    return f"hailofilter so-path={RESOURCES}/libyolo_hailortpp_post.so {labels} qos=false ! "


def HAILO_OVERLAY() -> str:
    return "hailooverlay ! "


class PipelineString(object):
    def __init__(self, network: str, source_type: str, video_source: str, show_display: bool, show_fps: bool):
        self.hef_path = self.__get_hef_path(network)
        self.source_type = source_type
        self.video_source = video_source
        self.video_sink = "xvimagesink" if show_display else "fakesink"
        self.show_fps = show_fps

        self.batch_size = 2
        self.network_width = 640
        self.network_height = 640
        self.network_format = "RGB"
        self.labels_config = '' if True else f' config-path="params.labels_json"'
        self.sync = "false"
        self.nms_score_threshold = 0.3
        self.nms_iou_threshold = 0.45

    def get_pipeline_string(self) -> str:
        return ("hailomuxer name=hmux " + self.__source() +
                QUEUE("queue_scale") + VIDEO_SCALE(threads=2) +
                QUEUE("queue_src_convert") + VIDEO_CONVERT(threads=3, name='src_convert', qos='false', format=self.network_format, width=self.network_width,
                                                           height=self.network_height, pixel_aspect_ratio='1/1') +

                TEE(variable='t') +
                QUEUE("bypass_queue", max_size_buffers=20) + "hmux.sink_0 t. ! " +
                QUEUE("queue_hailonet") + VIDEO_CONVERT(threads=3) + HAILO_NET(hef_path=self.hef_path,
                                                                               batch_size=self.batch_size,
                                                                               nms_score=self.nms_score_threshold,
                                                                               nms_iou=self.nms_iou_threshold) +
                QUEUE("queue_hailofilter") + HAILO_FILTER(labels=self.labels_config) +
                QUEUE("queue_hmuc") + "hmux.sink_1 hmux. ! " +
                QUEUE("queue_hailo_python") +
                QUEUE("queue_user_callback") + "identity name=identity_callback ! " +
                QUEUE("queue_hailooverlay") + HAILO_OVERLAY() +
                QUEUE("queue_videoconvert") + VIDEO_CONVERT(threads=3, qos='false') +
                QUEUE("queue_hailo_display") + FPS_DISPLAY_SINK(video_sink=self.video_sink, sync=self.sync, show_fps=self.show_fps))

    def __source(self) -> str:
        match self.source_type:
            case "rpi":
                return (f"libcamerasrc name=src_0 ! " + VIDEO_RAW(format=self.network_format, width=1536, height=864) +
                        QUEUE("queue_src_scale") + VIDEO_SCALE(framerate='30/1',
                                                               format=self.network_format,
                                                               width=self.network_width,
                                                               height=self.network_height))
            case "usb":
                return f"v4l2src device={self.video_source} name=src_0 ! " + VIDEO_RAW(framerate='30/1', width=640, height=480)

            case _:
                return (f'filesrc location="{self.video_source}" name=src_0 ! ' +
                        QUEUE("queue_dec264") + "qtdemux ! h264parse ! avdec_h264 max-threads=2 ! " + VIDEO_RAW(format='I420'))

    @staticmethod
    def __get_hef_path(network: str):
        if network == "yolov6n":
            return f'{RESOURCES}/yolov6n.hef'
        elif network == "yolov8s":
            return f'{RESOURCES}/yolov8s_h8l.hef'
        elif network == "yolox_s_leaky":
            return f'{RESOURCES}/yolox_s_leaky_h8l_mz.hef'

        assert False, f"Invalid network type: {network}!"
