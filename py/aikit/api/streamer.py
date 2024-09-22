import gi

gi.require_version('Gst', '1.0')  # define before importing Gst

from gi.repository import Gst, GLib
from py.aikit.api.pipeline import Pipeline

import logging
import multiprocessing
import signal

log = logging.getLogger(__name__)


class HailoGStreamer:
    class Data(object):
        def __init__(self):
            self.frame_count = 0
            self.frame_queue = multiprocessing.Queue(maxsize=3)  # set up a multiprocessing queue to pass the frame to the main thread
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

    def __init__(self, source_type: str, video_input: str, show_fps: bool, data: Data, on_probe_callback, pipeline_string: str):
        self.source_type = source_type
        self.video_source = video_input
        self.data = data
        self.on_probe_callback = on_probe_callback
        self.pipeline = Pipeline(pipeline_string, show_fps)
        self.loop = GLib.MainLoop()

        # Set up signal handler for SIGINT (Ctrl-C)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self) -> None:
        log.info("GStreamer started!")

        self.pipeline.add_watch_to_bus(self.__bus_call, self.loop)
        self.pipeline.connect_pad_probe_to_identity_element(self.on_probe_callback, self.data)
        self.pipeline.disable_qos()
        self.pipeline.change_state_to(Gst.State.PLAYING)

        self.loop.run()  # Run the GLib event loop

        # Clean up
        self.data.running = False
        self.pipeline.cleanup()

    def __bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            log.warning("End-of-stream")
            self.__on_eos()
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

    def __on_eos(self):
        if self.source_type == "file":
            # Seek to the start (position 0) in nanoseconds
            success = self.pipeline.seek_simple()
            if success:
                log.warning("Video rewound successfully. Restarting playback...")
            else:
                log.error("Error rewinding the video.")
        else:
            self.shutdown()

    def shutdown(self, signum=None, frame=None):
        log.warning("Shutting down... Hit Ctrl-C again to force quit.")

        signal.signal(signal.SIGINT, signal.SIG_DFL)

        self.pipeline.change_state_to(Gst.State.PAUSED)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.change_state_to(Gst.State.READY)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.change_state_to(Gst.State.NULL)
        GLib.idle_add(self.loop.quit)
