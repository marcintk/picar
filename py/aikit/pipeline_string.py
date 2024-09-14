import os


class PipelineString(object):
    def __init__(self, network: str, video_source: str, show_display: bool, show_fps: bool):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.video_source = video_source
        self.source_type = self.get_source_type(video_source)
        self.show_fps = show_fps
        self.hef_path = self.__get_hef_path(network)
        self.batch_size = 2
        self.network_width = 640
        self.network_height = 640
        self.network_format = "RGB"
        self.nms_score_threshold = 0.3
        self.nms_iou_threshold = 0.45
        self.labels_config = '' if True else f' config-path="params.labels_json"'
        self.video_sink = "xvimagesink" if show_display else "fakesink"
        self.sync = "false"

        # Temporary code: new postprocess will be merged to TAPPAS.
        # Check if new postprocess so file exists
        self.default_postprocess_so = os.path.join(self.current_path, './resources/libyolo_hailortpp_post.so')

        self.thresholds_str = (f"nms-score-threshold={self.nms_score_threshold} "
                               f"nms-iou-threshold={self.nms_iou_threshold} "
                               f"output-format-type=HAILO_FORMAT_TYPE_FLOAT32")

        print('model', network)

    def get_pipeline_string(self) -> str:
        if self.source_type == "rpi":
            source_element = ("libcamerasrc name=src_0 ! "
                              f"video/x-raw, format={self.network_format}, width=1536, height=864 ! " + self.QUEUE("queue_src_scale") + "videoscale ! "
                                                                                                                                        f"video/x-raw, format={self.network_format}, width={self.network_width}, height={self.network_height}, framerate=30/1 ! ")
        elif self.source_type == "usb":
            source_element = (f"v4l2src device={self.video_source} name=src_0 ! "
                              "video/x-raw, width=640, height=480, framerate=30/1 ! ")
        else:
            source_element = (
                    f"filesrc location=\"{self.video_source}\" name=src_0 ! " + self.QUEUE("queue_dec264") + " qtdemux ! h264parse ! avdec_h264 max-threads=2 ! "
                                                                                                             " video/x-raw, format=I420 ! ")
        source_element += self.QUEUE("queue_scale")
        source_element += "videoscale n-threads=2 ! "
        source_element += self.QUEUE("queue_src_convert")
        source_element += "videoconvert n-threads=3 name=src_convert qos=false ! "
        source_element += f"video/x-raw, format={self.network_format}, width={self.network_width}, height={self.network_height}, pixel-aspect-ratio=1/1 ! "

        pipeline_string = ("hailomuxer name=hmux " + source_element + "tee name=t ! " + self.QUEUE("bypass_queue",
                                                                                                   max_size_buffers=20) + "hmux.sink_0 " + "t. ! " + self.QUEUE(
            "queue_hailonet") + "videoconvert n-threads=3 ! "
                                f"hailonet hef-path={self.hef_path} batch-size={self.batch_size} {self.thresholds_str} force-writable=true ! " + self.QUEUE(
            "queue_hailofilter") + f"hailofilter so-path={self.default_postprocess_so} {self.labels_config} qos=false ! " + self.QUEUE("queue_hmuc") + "hmux.sink_1 " + "hmux. ! " + self.QUEUE(
            "queue_hailo_python") + self.QUEUE("queue_user_callback") + "identity name=identity_callback ! " + self.QUEUE("queue_hailooverlay") + "hailooverlay ! " + self.QUEUE(
            "queue_videoconvert") + "videoconvert n-threads=3 qos=false ! " + self.QUEUE("queue_hailo_display") + f"fpsdisplaysink video-sink={self.video_sink} name=hailo_display sync={self.sync} text-overlay={self.show_fps} signal-fps-measurements=true ")
        print(pipeline_string)
        return pipeline_string

    def __get_hef_path(self, network: str):
        # Set the HEF file path based on the network
        if network == "yolov6n":
            return os.path.join(self.current_path, './resources/yolov6n.hef')
        elif network == "yolov8s":
            return os.path.join(self.current_path, './resources/yolov8s_h8l.hef')
        elif network == "yolox_s_leaky":
            return os.path.join(self.current_path, './resources/yolox_s_leaky_h8l_mz.hef')
        else:
            assert False, "Invalid network type"

    @staticmethod
    def get_source_type(video_source: str):
        # This function will return the source type based on the input source
        # return values can be "file", "mipi" or "usb"
        if video_source.startswith("/dev/video"):
            return 'usb'
        else:
            if video_source.startswith("rpi"):
                return 'rpi'
            else:
                return 'file'

    @staticmethod
    def QUEUE(name, max_size_buffers=3, max_size_bytes=0, max_size_time=0, leaky='no'):
        return f"queue name={name} leaky={leaky} max-size-buffers={max_size_buffers} max-size-bytes={max_size_bytes} max-size-time={max_size_time} ! "
