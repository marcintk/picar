import gi

from py.aikit.api.data import HailoData
from py.aikit.frame_rate import FrameRate
from py.exchange_data import ExchangeData

gi.require_version('Gst', '1.0')  # define before importing Gst

from gi.repository import Gst
from py.aikit.api.commons import (get_caps_from_pad, )
from py.aikit.api.pipeline_string import PipelineString
from py.aikit.api.streamer import HailoGStreamer
from py.multiprocessor import MultiProcessor
from py.params import Parameters

import logging
import hailo

log = logging.getLogger(__name__)


class AiDetector(HailoGStreamer, MultiProcessor.Runner):
    def __init__(self, params: Parameters, data: HailoData):
        super().__init__(source_type=params.get_source_type(),
                         video_input=params.video_input,
                         show_fps=params.show_fps,
                         data=data,
                         pipeline_string=PipelineString(network=params.network,
                                                        source_type=params.get_source_type(),
                                                        video_source=params.video_input,
                                                        show_display=params.show_display,
                                                        show_fps=params.show_fps).get_pipeline_string())
        self.fps = FrameRate()

    def on_probe(self, pad, info, data: ExchangeData):

        buffer = info.get_buffer()  # Get the GstBuffer from the probe info

        if buffer is None:  # Check if the buffer is valid
            return Gst.PadProbeReturn.OK

        # Using the user_data to count the number of frames
        data.increment()

        # Calculate frames per second
        (rate, last_changed, last_rate) = self.fps.probe()

        # Get the caps from the pad
        (format, width, height) = get_caps_from_pad(pad)

        # Get the detections from the buffer
        roi = hailo.get_roi_from_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)
        detection_count = self.__detect_persons(detections)
        data.new_persons_detected(9 if detection_count > 9 else detection_count)

        if last_changed:
            log.info(f'>> '
                     f'frame count:{data.get_count()} '
                     f'|| fps:{last_rate:.2f} (overall:{rate:.1f})'
                     f', detected:{detection_count}.')

        return Gst.PadProbeReturn.OK

    @staticmethod
    def __detect_persons(detections):
        detection_count = 0
        for detection in detections:
            label = detection.get_label()
            bbox = detection.get_bbox()
            confidence = detection.get_confidence()

            if label == "person":
                detection_count += 1

        return detection_count
