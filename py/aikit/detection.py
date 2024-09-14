import gi

from py.aikit.pipeline_string import PipelineString
from py.multiprocessor import MultiProcessorRunner
from py.params import Parameters

gi.require_version('Gst', '1.0')
from gi.repository import Gst
import hailo
from py.aikit.hailo_rpi_common import (get_caps_from_pad, GStreamerApp, GStreamerCallbackClass, )


# -----------------------------------------------------------------------------------------------
# User Gstreamer Application
# -----------------------------------------------------------------------------------------------

# This class inherits from the hailo_rpi_common.GStreamerApp class
class GStreamerDetectionApp(GStreamerApp, MultiProcessorRunner):
    def __init__(self, params: Parameters, user_data: GStreamerCallbackClass):
        # Call the parent class constructor
        super().__init__(params, user_data, self.callback_function)

        print('model', self.params.network)
        self.create_pipeline()

    def get_pipeline_string(self) -> str:
        return PipelineString(network=self.params.network,
                              video_source=self.params.video_input,
                              show_display=self.params.show_display,
                              show_fps=self.params.show_fps).get_pipeline_string()

    # -----------------------------------------------------------------------------------------------
    # User-defined callback function
    # -----------------------------------------------------------------------------------------------

    @staticmethod
    # This is the callback function that will be called when data is available from the pipeline
    def callback_function(pad, info, user_data):
        # Get the GstBuffer from the probe info
        buffer = info.get_buffer()
        # Check if the buffer is valid
        if buffer is None:
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

        print(string_to_print)
        return Gst.PadProbeReturn.OK
