RESOURCES = './py/aikit/api/resources'
HAILO_POST_SO = 'libyolo_hailortpp_post.so'


def QUEUE(name, max_size_buffers: int = 3, max_size_bytes: int = 0, max_size_time: int = 0, leaky: str = 'no', chains: list[str] = ()) -> str:
    return (
        f"queue name=queue_{name} leaky={leaky} max-size-buffers={max_size_buffers} max-size-bytes={max_size_bytes} max-size-time={max_size_time} ! "
        f"{''.join(chains)}")


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


def TEE(variable: str, sinks: list[str]) -> str:
    return f"tee name={variable} ! {''.join(sinks)}"


def TEE_SINK(from_queue: str, muxer: str, tee: str, sink_id: int, sinks: int, chains: list[str]) -> str:
    return "{}{}.sink_{} {}. ! {}".format(from_queue, muxer, sink_id, muxer if (sinks == sink_id + 1) else tee, ''.join(chains))


def FPS_DISPLAY_SINK(video_sink: str, sync: str, show_fps: bool) -> str:
    return f"fpsdisplaysink video-sink={video_sink} name=hailo_display sync={sync} text-overlay={show_fps} signal-fps-measurements=true"


def IDENTITY() -> str:
    return "identity name=identity_callback ! "


def HAILO_MUXER(variable: str, parent: str) -> str:
    return f"hailomuxer name={variable} {parent}"


def HAILO_NET(hef_path: str, batch_size: int, nms_score: float, nms_iou: float) -> str:
    return (f"hailonet hef-path={hef_path} batch-size={batch_size} nms-score-threshold={nms_score} nms-iou-threshold={nms_iou} "
            f"output-format-type=HAILO_FORMAT_TYPE_FLOAT32 force-writable=true ! ")


def HAILO_FILTER(labels: str) -> str:
    return "hailofilter so-path={}{} qos=false ! ".format(f'{RESOURCES}/{HAILO_POST_SO}',
                                                          f' config-path={labels}' if len(labels) > 0 else '')


def HAILO_OVERLAY() -> str:
    return "hailooverlay ! "


class PipelineString(object):
    def __init__(self, network: str, source_type: str, video_source: str, show_display: bool, show_fps: bool) -> None:
        self.hef_path = self.__get_hef_path(network)
        self.source_type = source_type
        self.video_source = video_source
        self.video_sink = "xvimagesink" if show_display else "fakesink"
        self.show_fps = show_fps

        self.batch_size = 2
        self.network_width = 640
        self.network_height = 640
        self.network_format = "RGB"
        self.nms_score_threshold = 0.3
        self.nms_iou_threshold = 0.45
        self.labels_config = ''
        self.sync = "false"

    def get_pipeline_string(self) -> str:
        muxer_variable = 'hmuc'
        tee_variable = 't'

        return (HAILO_MUXER(variable=muxer_variable, parent=self.__source()) +
                QUEUE("scale", chains=[VIDEO_SCALE(threads=2)]) +
                QUEUE("src_convert", chains=[VIDEO_CONVERT(threads=3,
                                                           name='src_convert',
                                                           qos='false',
                                                           format=self.network_format,
                                                           width=self.network_width,
                                                           height=self.network_height,
                                                           pixel_aspect_ratio='1/1')]) +

                TEE(variable=tee_variable,
                    sinks=[TEE_SINK(from_queue=QUEUE("bypass", max_size_buffers=20),
                                    muxer=muxer_variable,
                                    tee=tee_variable,
                                    sink_id=0,
                                    sinks=2,
                                    chains=[QUEUE("hailonet",
                                                  chains=[VIDEO_CONVERT(threads=3),
                                                          HAILO_NET(hef_path=self.hef_path,
                                                                    batch_size=self.batch_size,
                                                                    nms_score=self.nms_score_threshold,
                                                                    nms_iou=self.nms_iou_threshold)]),
                                            QUEUE("hailofilter", chains=[HAILO_FILTER(labels=self.labels_config)])]),
                           TEE_SINK(from_queue=QUEUE(muxer_variable),
                                    muxer=muxer_variable,
                                    tee=tee_variable,
                                    sink_id=1,
                                    sinks=2,
                                    chains=[QUEUE("hailo_python"),
                                            QUEUE("user_callback", chains=[IDENTITY()]),
                                            QUEUE("hailooverlay", chains=[HAILO_OVERLAY()]),
                                            QUEUE("videoconvert", chains=[VIDEO_CONVERT(threads=3, qos='false')]),
                                            QUEUE("hailo_display", chains=[FPS_DISPLAY_SINK(video_sink=self.video_sink,
                                                                                            sync=self.sync,
                                                                                            show_fps=self.show_fps)])])]))

    def __source(self, name: str = 'src') -> str:
        match self.source_type:
            case "rpi":
                return (f"libcamerasrc name={name}_0 ! " + VIDEO_RAW(format=self.network_format, width=1536, height=864) +
                        QUEUE("src_scale",
                              chains=[VIDEO_SCALE(framerate='30/1', format=self.network_format, width=self.network_width, height=self.network_height)]))
            case "usb":
                return f"v4l2src device={self.video_source} name={name}_0 ! " + VIDEO_RAW(framerate='30/1', width=640, height=480)

            case _:
                return (f'filesrc location="{self.video_source}" name={name}_0 ! ' +
                        QUEUE("dec264", chains=["qtdemux ! h264parse ! avdec_h264 max-threads=2 ! ", VIDEO_RAW(format='I420')]))

    @staticmethod
    def __get_hef_path(network: str) -> str:
        if network in ["yolov6n", "yolov8s", "yolov8s_pose"]:
            return f'{RESOURCES}/{network}.hef'

        assert False, f"Invalid network type: {network}!"
