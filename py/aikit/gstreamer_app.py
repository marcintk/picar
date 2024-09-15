import logging
import sys

import gi

from py.aikit.hailo_rpi_common import disable_qos

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib
import os
import multiprocessing
import setproctitle
import signal

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
class GStreamerApp:
    def __init__(self, source_type: str, video_input: str, show_fps: bool, shared_data: GStreamerData, on_probe_callback, pipeline_string: str):
        self.source_type = source_type
        self.video_source = video_input
        self.shared_data = shared_data
        self.on_probe_callback = on_probe_callback
        self.pipeline = self.__create_pipeline(pipeline_string, show_fps)
        self.loop = GLib.MainLoop()

        # Set up signal handler for SIGINT (Ctrl-C)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self) -> None:
        log.info("GStreamer started!")

        # Add a watch for messages on the pipeline's bus
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call, self.loop)

        # Connect pad probe to the identity element
        identity = self.pipeline.get_by_name("identity_callback")
        if identity is None:
            log.warning(
                "Warning: identity_callback element not found, add <identity name=identity_callback> in your pipeline where you want the callback to be called.")
        else:
            identity_pad = identity.get_static_pad("src")
            identity_pad.add_probe(Gst.PadProbeType.BUFFER, self.on_probe_callback, self.shared_data)

        # Get xvimagesink element and disable QoS
        # xvimagesink is instantiated by fpsdisplaysink
        hailo_display = self.pipeline.get_by_name("hailo_display")
        if hailo_display is None:
            log.warning("Warning: hailo_display element not found, add <fpsdisplaysink name=hailo_display> to your pipeline to support fps display.")
        else:
            xvimagesink = hailo_display.get_by_name("xvimagesink0")
            if xvimagesink is not None:
                xvimagesink.set_property("qos", False)

        # Disable QoS to prevent frame drops
        disable_qos(self.pipeline)

        # Set pipeline to PLAYING state
        self.pipeline.set_state(Gst.State.PLAYING)

        # Run the GLib event loop
        self.loop.run()

        # Clean up
        self.shared_data.running = False
        self.pipeline.set_state(Gst.State.NULL)

    def bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            log.warning("End-of-stream")
            self.on_eos()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, {debug}")
            self.shutdown()
        # QOS
        elif t == Gst.MessageType.QOS:
            # Handle QoS message here
            qos_element = message.src.get_name()
            log.warning(f"QoS message received from {qos_element}")
        return True

    def on_eos(self):
        if self.source_type == "file":
            # Seek to the start (position 0) in nanoseconds
            success = self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 0)
            if success:
                log.warning("Video rewound successfully. Restarting playback...")
            else:
                log.error("Error rewinding the video.")
        else:
            self.shutdown()

    def shutdown(self, signum=None, frame=None):
        log.warning("Shutting down... Hit Ctrl-C again to force quit.")

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.pipeline.set_state(Gst.State.PAUSED)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.READY)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.NULL)
        GLib.idle_add(self.loop.quit)

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
                pipeline.get_by_name("hailo_display").connect("fps-measurements", GStreamerApp.on_fps_measurement)

            return pipeline
        except Exception as e:
            log.error(e)
            log.error(pipeline_string)
            sys.exit(1)

    @staticmethod
    def on_fps_measurement(sink, fps, droprate, avgfps):
        print(f"FPS: {fps:.2f}, Droprate: {droprate:.2f}, Avg FPS: {avgfps:.2f}")
        return True

    @staticmethod
    def __get_tappas_postprocess_dir():
        tappas_postprocess_dir = os.environ.get('TAPPAS_POST_PROC_DIR', '')
        if tappas_postprocess_dir == '':
            log.warning("TAPPAS_POST_PROC_DIR environment variable is not set. Please set it to by sourcing setup_env.sh")
            exit(1)
        return tappas_postprocess_dir
