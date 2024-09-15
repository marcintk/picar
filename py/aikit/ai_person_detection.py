import logging

import gi
import hailo
from gi.repository import Gst

from py.aikit.api.commons import (get_caps_from_pad, )
from py.aikit.api.pipeline_string import PipelineString
from py.aikit.api.streamer import HailoGStreamer
from py.multiprocessor import MultiProcessor
from py.params import Parameters

gi.require_version('Gst', '1.0')

log = logging.getLogger(__name__)


class AiPersonDetector(HailoGStreamer, MultiProcessor.Runner):
    def __init__(self, params: Parameters, shared_data: HailoGStreamer.Data):
        super().__init__(source_type=params.get_source_type(),
                         video_input=params.video_input,
                         show_fps=params.show_fps,
                         shared_data=shared_data,
                         on_probe_callback=AiPersonDetector.on_probe,
                         pipeline_string=PipelineString(network=params.network,
                                                        source_type=params.get_source_type(),
                                                        video_source=params.video_input,
                                                        show_display=params.show_display,
                                                        show_fps=params.show_fps).get_pipeline_string())

    # -----------------------------------------------------------------------------------------------
    # User-defined callback function
    # This is the callback function that will be called when data is available from the pipeline
    # -----------------------------------------------------------------------------------------------

    @staticmethod
    def on_probe(pad, info, user_data):
        buffer = info.get_buffer()  # Get the GstBuffer from the probe info

        if buffer is None:  # Check if the buffer is valid
            return Gst.PadProbeReturn.OK

        # Using the user_data to count the number of frames
        user_data.increment()
        string_to_print = f"Frame count: {user_data.get_count()}\n"

        # Get the caps from the pad
        format, width, height = get_caps_from_pad(pad)

        # Get the detections from the buffer
        roi = hailo.get_roi_from_buffer(buffer)
        detections = roi.get_objects_typed(hailo.HAILO_DETECTION)

        # Parse the detections
        detection_count = 0
        for detection in detections:
            label = detection.get_label()
            bbox = detection.get_bbox()
            confidence = detection.get_confidence()

            if label == "person":
                string_to_print += f"Detection: {label} {confidence:.2f}\n"
                detection_count += 1

        if detection_count > 0:
            user_data.detected.value = 9 if detection_count > 9 else detection_count
        else:
            user_data.detected.value = 0

        log.debug(string_to_print)
        return Gst.PadProbeReturn.OK
