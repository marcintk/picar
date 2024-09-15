import logging
import sys

import gi

from py.aikit.api.commons import disable_qos

gi.require_version('Gst', '1.0')
from gi.repository import Gst
import multiprocessing
import setproctitle

log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# A sample class to be used in the callback function
# This example allows to:
# 1. Count the number of frames
# 2. Setup a multiprocessing queue to pass the frame to the main thread
# Additional variables and functions can be added to this class as needed

class GStreamerData(object):
    def __init__(self):
        self.frame_count = 0
        self.frame_queue = multiprocessing.Queue(maxsize=3)
        self.running = True

    def increment(self):
        self.frame_count += 1

    def get_count(self):
        return self.frame_count

    def set_frame(self, frame):
        if not self.frame_queue.full():
            self.frame_queue.put(frame)

    def get_frame(self):
        return None if self.frame_queue.empty() else self.frame_queue.get()


# -----------------------------------------------------------------------------------------------
# GStreamerApp class
# -----------------------------------------------------------------------------------------------
class Pipeline:

    def __init__(self, pipeline_string: str, show_fps: bool):
        self.pipeline = self.__create_pipeline(pipeline_string, show_fps)

    # Add a watch for messages on the pipeline's bus
    def add_watch_to_bus(self, bus_call, loop) -> None:
        bus = self.pipeline.setup_bus()
        bus.add_signal_watch()
        bus.connect("message", bus_call, loop)

    # Connect pad probe to the identity element
    def connect_pad_probe_to_identity_element(self, on_probe_callback, shared_data) -> None:
        identity = self.pipeline.get_by_name("identity_callback")
        if identity is None:
            log.warning(
                "Warning: identity_callback element not found, add <identity name=identity_callback> in your pipeline where you want the callback to be "
                "called.")
        else:
            identity_pad = identity.get_static_pad("src")
            identity_pad.add_probe(Gst.PadProbeType.BUFFER, on_probe_callback, shared_data)

    def disable_qos(self) -> None:
        hailo_display = self.pipeline.get_by_name("hailo_display")
        if hailo_display is None:
            log.warning("Warning: hailo_display element not found, add <fpsdisplaysink name=hailo_display> to your pipeline to support fps display.")
        else:
            xvimagesink = hailo_display.get_by_name("xvimagesink0")
            if xvimagesink is not None:
                xvimagesink.set_property("qos", False)

        # Disable QoS to prevent frame drops
        disable_qos(self.pipeline)

    def change_state_to(self, state: Gst.State):
        self.pipeline.set_state(state)

    def seek_simple(self):
        self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 0)

    def cleanup(self) -> None:
        self.pipeline.set_state(Gst.State.NULL)

    @staticmethod
    def __create_pipeline(pipeline_string: str, show_fps: bool):
        try:
            # Set the process title
            setproctitle.setproctitle("Hailo Python Application")

            # Initialize GStreamer
            Gst.init(None)

            pipeline = Gst.parse_launch(pipeline_string)

            # Connect to hailo_display fps-measurements
            if show_fps:
                log.info("Showing FPS")
                pipeline.get_by_name("hailo_display").connect("fps-measurements", Pipeline.on_fps_measurement)

            return pipeline
        except Exception as e:
            log.error(e)
            log.error(pipeline_string)
            sys.exit(1)

    @staticmethod
    def on_fps_measurement(sink, fps, droprate, avgfps):
        print(f"FPS: {fps:.2f}, Droprate: {droprate:.2f}, Avg FPS: {avgfps:.2f}")
        return True  # @staticmethod  # def __get_tappas_postprocess_dir():  #     tappas_postprocess_dir = os.environ.get('TAPPAS_POST_PROC_DIR',
        # '')  #     if tappas_postprocess_dir == '':  #         log.warning("TAPPAS_POST_PROC_DIR environment variable is not set. Please set it to by
        # sourcing setup_env.sh")  #         exit(1)  #     return tappas_postprocess_dir
