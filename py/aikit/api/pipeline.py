import gi

from py.aikit.api.data import HailoData

gi.require_version('Gst', '1.0')  # define before importing Gst

from gi.repository import Gst
from py.aikit.api.commons import disable_qos

import logging
import sys
import setproctitle

log = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------
# GStreamerApp class
# -----------------------------------------------------------------------------------------------
class Pipeline:
    def __init__(self, pipeline_string: str, show_fps: bool):
        self.pipeline = self.__create_pipeline(pipeline_string, show_fps)

    # Add a watch for messages on the pipeline's bus
    def add_watch_to_bus(self, bus_call, loop) -> None:
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", bus_call, loop)

    # Connect pad probe to the identity element
    def connect_pad_probe_to_identity_element(self, on_probe_callback, data: HailoData) -> None:
        identity = self.pipeline.get_by_name("identity_callback")
        if identity is None:
            log.warning("identity_callback element not found, add <identity name=identity_callback> in your pipeline where you want the callback to be called.")
        else:
            identity_pad = identity.get_static_pad("src")
            identity_pad.add_probe(Gst.PadProbeType.BUFFER, on_probe_callback, data)

    # Disable QoS to prevent frame drops
    def disable_qos(self) -> None:
        hailo_display = self.pipeline.get_by_name("hailo_display")
        if hailo_display is None:
            log.warning("hailo_display element not found, add <fpsdisplaysink name=hailo_display> to your pipeline to support fps display.")
        else:
            xvimagesink = hailo_display.get_by_name("xvimagesink0")
            if xvimagesink is not None:
                xvimagesink.set_property("qos", False)

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
            setproctitle.setproctitle("Hailo Python Application")

            Gst.init(None)  # Initialize GStreamer

            pipeline = Gst.parse_launch(pipeline_string)

            log.info('pipeline_string:\n%s', pipeline_string)

            # Connect to hailo_display fps-measurements
            if show_fps:
                log.info("Showing FPS activated.")
                pipeline.get_by_name("hailo_display").connect("fps-measurements", Pipeline.on_fps_measurement)

            return pipeline
        except Exception as e:
            log.error(e)
            log.error(pipeline_string)
            sys.exit(1)

    @staticmethod
    def on_fps_measurement(sink, fps, droprate, avgfps):
        log.info(f"FPS: {fps:.2f}, Droprate: {droprate:.2f}, Avg FPS: {avgfps:.2f}")
        return True
