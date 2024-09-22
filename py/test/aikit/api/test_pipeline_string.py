from unittest import TestCase

from py.aikit.api.pipeline_string import PipelineString


class TestPipelineString(TestCase):
    def test_get_pipeline_string_rpi(self) -> None:
        self.__test(source_type='rpi',
                    expected=(
                        "hailomuxer name=hmuc libcamerasrc name=src_0 ! video/x-raw, format=RGB, width=1536, height=864 ! queue name=queue_src_scale leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoscale ! video/x-raw, framerate=30/1, format=RGB, width=640, "
                        "height=640 ! queue name=queue_scale leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoscale n-threads=2 ! queue "
                        "name=queue_src_convert leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 name=src_convert "
                        "qos=false ! video/x-raw, format=RGB, width=640, height=640, pixel-aspect-ratio=1/1 ! tee name=t ! queue name=queue_bypass leaky=no "
                        "max-size-buffers=20 max-size-bytes=0 max-size-time=0 ! hmuc.sink_0 t. ! queue name=queue_hailonet leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 ! hailonet hef-path=./py/aikit/api/resources//yolov6n.hef batch-size=2 "
                        "nms-score-threshold=0.3 nms-iou-threshold=0.45 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 force-writable=true ! queue "
                        "name=queue_hailofilter leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailofilter "
                        "so-path=./py/aikit/api/resources//libyolo_hailortpp_post.so qos=false ! queue name=queue_hmuc leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! hmuc.sink_1 hmuc. ! queue name=queue_hailo_python leaky=no max-size-buffers=3 max-size-bytes=0 "
                        "max-size-time=0 ! queue name=queue_user_callback leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! identity "
                        "name=identity_callback ! queue name=queue_hailooverlay leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailooverlay ! "
                        "queue name=queue_videoconvert leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 qos=false ! "
                        "queue name=queue_hailo_display leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! fpsdisplaysink video-sink=xvimagesink "
                        "name=hailo_display sync=false text-overlay=True signal-fps-measurements=true"))

    def test_get_pipeline_string_usb(self) -> None:
        self.__test(source_type='usb',
                    expected=(
                        "hailomuxer name=hmuc v4l2src device=file name=src_0 ! video/x-raw, framerate=30/1, width=640, height=480 ! queue name=queue_scale "
                        "leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoscale n-threads=2 ! queue name=queue_src_convert leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 name=src_convert qos=false ! video/x-raw, format=RGB, "
                        "width=640, height=640, pixel-aspect-ratio=1/1 ! tee name=t ! queue name=queue_bypass leaky=no max-size-buffers=20 max-size-bytes=0 "
                        "max-size-time=0 ! hmuc.sink_0 t. ! queue name=queue_hailonet leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! "
                        "videoconvert n-threads=3 ! hailonet hef-path=./py/aikit/api/resources//yolov6n.hef batch-size=2 nms-score-threshold=0.3 "
                        "nms-iou-threshold=0.45 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 force-writable=true ! queue name=queue_hailofilter leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailofilter so-path=./py/aikit/api/resources//libyolo_hailortpp_post.so "
                        "qos=false ! queue name=queue_hmuc leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hmuc.sink_1 hmuc. ! queue "
                        "name=queue_hailo_python leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! queue name=queue_user_callback leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! identity name=identity_callback ! queue name=queue_hailooverlay leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailooverlay ! queue name=queue_videoconvert leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 qos=false ! queue name=queue_hailo_display leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! fpsdisplaysink video-sink=xvimagesink name=hailo_display sync=false text-overlay=True "
                        "signal-fps-measurements=true"))

    def test_get_pipeline_string_other(self) -> None:
        self.__test(source_type='other',
                    expected=(
                        "hailomuxer name=hmuc filesrc location=\"file\" name=src_0 ! queue name=queue_dec264 leaky=no max-size-buffers=3 max-size-bytes=0 "
                        "max-size-time=0 ! qtdemux ! h264parse ! avdec_h264 max-threads=2 ! video/x-raw, format=I420 ! queue name=queue_scale leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoscale n-threads=2 ! queue name=queue_src_convert leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 name=src_convert qos=false ! video/x-raw, format=RGB, "
                        "width=640, height=640, pixel-aspect-ratio=1/1 ! tee name=t ! queue name=queue_bypass leaky=no max-size-buffers=20 max-size-bytes=0 "
                        "max-size-time=0 ! hmuc.sink_0 t. ! queue name=queue_hailonet leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! "
                        "videoconvert n-threads=3 ! hailonet hef-path=./py/aikit/api/resources//yolov6n.hef batch-size=2 nms-score-threshold=0.3 "
                        "nms-iou-threshold=0.45 output-format-type=HAILO_FORMAT_TYPE_FLOAT32 force-writable=true ! queue name=queue_hailofilter leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailofilter so-path=./py/aikit/api/resources//libyolo_hailortpp_post.so "
                        "qos=false ! queue name=queue_hmuc leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hmuc.sink_1 hmuc. ! queue "
                        "name=queue_hailo_python leaky=no max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! queue name=queue_user_callback leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! identity name=identity_callback ! queue name=queue_hailooverlay leaky=no "
                        "max-size-buffers=3 max-size-bytes=0 max-size-time=0 ! hailooverlay ! queue name=queue_videoconvert leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! videoconvert n-threads=3 qos=false ! queue name=queue_hailo_display leaky=no max-size-buffers=3 "
                        "max-size-bytes=0 max-size-time=0 ! fpsdisplaysink video-sink=xvimagesink name=hailo_display sync=false text-overlay=True "
                        "signal-fps-measurements=true"))

    def __test(self, source_type: str, expected: str) -> None:
        actual = PipelineString(network='yolov6n', source_type=source_type, video_source='file', show_display=True, show_fps=True).get_pipeline_string()
        self.assertEqual(actual, expected, msg=f'invalid: {actual}')
