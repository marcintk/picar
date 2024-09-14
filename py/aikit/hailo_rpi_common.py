import sys

import gi

from py.params import Parameters

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib, GObject
import os
import multiprocessing
import numpy as np
import setproctitle
import cv2
import signal

# Try to import hailo python module
try:
    import hailo
except ImportError:
    sys.exit("Failed to import hailo python module. Make sure you are in hailo virtual environment.")


# -----------------------------------------------------------------------------------------------
# User-defined class to be used in the callback function
# -----------------------------------------------------------------------------------------------
# A sample class to be used in the callback function
# This example allows to:
# 1. Count the number of frames
# 2. Setup a multiprocessing queue to pass the frame to the main thread
# Additional variables and functions can be added to this class as needed

class GStreamerCallbackClass(object):
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
# Common functions
# -----------------------------------------------------------------------------------------------
def get_caps_from_pad(pad: Gst.Pad):
    caps = pad.get_current_caps()
    if caps:
        # We can now extract information from the caps
        structure = caps.get_structure(0)
        if structure:
            # Extracting some common properties
            format = structure.get_value('format')
            width = structure.get_value('width')
            height = structure.get_value('height')
            return format, width, height
    else:
        return None, None, None


# This function is used to display the user data frame
def display_user_data_frame(user_data: GStreamerCallbackClass):
    while user_data.running:
        frame = user_data.get_frame()
        if frame is not None:
            cv2.imshow("User Frame", frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()


def get_source_type(input_source):
    # This function will return the source type based on the input source
    # return values can be "file", "mipi" or "usb"
    if input_source.startswith("/dev/video"):
        return 'usb'
    else:
        if input_source.startswith("rpi"):
            return 'rpi'
        else:
            return 'file'


# -----------------------------------------------------------------------------------------------
# GStreamerApp class
# -----------------------------------------------------------------------------------------------
class GStreamerApp:
    def __init__(self, params: Parameters, user_data: GStreamerCallbackClass, callback_function):
        self.params: Parameters = params
        self.app_callback = callback_function

        # Set the process title
        setproctitle.setproctitle("Hailo Python App")

        # Set up signal handler for SIGINT (Ctrl-C)
        signal.signal(signal.SIGINT, self.shutdown)

        # Initialize variables
        tappas_postprocess_dir = os.environ.get('TAPPAS_POST_PROC_DIR', '')
        if tappas_postprocess_dir == '':
            print("TAPPAS_POST_PROC_DIR environment variable is not set. Please set it to by sourcing setup_env.sh")
            exit(1)
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.postprocess_dir = tappas_postprocess_dir
        self.video_source = self.params.video_input
        self.source_type = get_source_type(self.video_source)
        self.user_data = user_data
        self.pipeline = None
        self.loop = None

    def on_fps_measurement(self, sink, fps, droprate, avgfps):
        print(f"FPS: {fps:.2f}, Droprate: {droprate:.2f}, Avg FPS: {avgfps:.2f}")
        return True

    def create_pipeline(self):
        # Initialize GStreamer
        Gst.init(None)

        pipeline_string = self.get_pipeline_string()
        try:
            self.pipeline = Gst.parse_launch(pipeline_string)
        except Exception as e:
            print(e)
            print(pipeline_string)
            sys.exit(1)

        # Connect to hailo_display fps-measurements
        if self.params.show_fps:
            print("Showing FPS")
            self.pipeline.get_by_name("hailo_display").connect("fps-measurements", self.on_fps_measurement)

        # Create a GLib Main Loop
        self.loop = GLib.MainLoop()

    def bus_call(self, bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            print("End-of-stream")
            self.on_eos()
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print(f"Error: {err}, {debug}")
            self.shutdown()
        # QOS
        elif t == Gst.MessageType.QOS:
            # Handle QoS message here
            qos_element = message.src.get_name()
            print(f"QoS message received from {qos_element}")
        return True

    def on_eos(self):
        if self.source_type == "file":
            # Seek to the start (position 0) in nanoseconds
            success = self.pipeline.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, 0)
            if success:
                print("Video rewound successfully. Restarting playback...")
            else:
                print("Error rewinding the video.")
        else:
            self.shutdown()

    def shutdown(self, signum=None, frame=None):
        print("Shutting down... Hit Ctrl-C again to force quit.")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.pipeline.set_state(Gst.State.PAUSED)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.READY)
        GLib.usleep(100000)  # 0.1 second delay

        self.pipeline.set_state(Gst.State.NULL)
        GLib.idle_add(self.loop.quit)

    def get_pipeline_string(self):
        # This is a placeholder function that should be overridden by the child class
        return ""

    def dump_dot_file(self):
        print("Dumping dot file...")
        Gst.debug_bin_to_dot_file(self.pipeline, Gst.DebugGraphDetails.ALL, "pipeline")
        return False

    def run(self) -> None:
        # Add a watch for messages on the pipeline's bus
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.bus_call, self.loop)

        # Connect pad probe to the identity element
        identity = self.pipeline.get_by_name("identity_callback")
        if identity is None:
            print(
                "Warning: identity_callback element not found, add <identity name=identity_callback> in your pipeline where you want the callback to be called.")
        else:
            identity_pad = identity.get_static_pad("src")
            identity_pad.add_probe(Gst.PadProbeType.BUFFER, self.app_callback, self.user_data)

        # Get xvimagesink element and disable QoS
        # xvimagesink is instantiated by fpsdisplaysink
        hailo_display = self.pipeline.get_by_name("hailo_display")
        if hailo_display is None:
            print("Warning: hailo_display element not found, add <fpsdisplaysink name=hailo_display> to your pipeline to support fps display.")
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
        self.user_data.running = False
        self.pipeline.set_state(Gst.State.NULL)


# ---------------------------------------------------------
# Functions used to get numpy arrays from GStreamer buffers
# ---------------------------------------------------------

def handle_rgb(map_info, width, height):
    # The copy() method is used to create a copy of the numpy array. This is necessary because the original numpy array is created from buffer data, and it does not own the data it represents. Instead, it's just a view of the buffer's data.
    return np.ndarray(shape=(height, width, 3), dtype=np.uint8, buffer=map_info.data).copy()


def handle_nv12(map_info, width, height):
    y_plane_size = width * height
    uv_plane_size = width * height // 2
    y_plane = np.ndarray(shape=(height, width), dtype=np.uint8, buffer=map_info.data[:y_plane_size]).copy()
    uv_plane = np.ndarray(shape=(height // 2, width // 2, 2), dtype=np.uint8, buffer=map_info.data[y_plane_size:]).copy()
    return y_plane, uv_plane


def handle_yuyv(map_info, width, height):
    return np.ndarray(shape=(height, width, 2), dtype=np.uint8, buffer=map_info.data).copy()


FORMAT_HANDLERS = {
    'RGB': handle_rgb, 'NV12': handle_nv12, 'YUYV': handle_yuyv,
}


def get_numpy_from_buffer(buffer, format, width, height):
    """
    Converts a GstBuffer to a numpy array based on provided format, width, and height.

    Args:
        buffer (GstBuffer): The GStreamer Buffer to convert.
        format (str): The video format ('RGB', 'NV12', 'YUYV', etc.).
        width (int): The width of the video frame.
        height (int): The height of the video frame.

    Returns:
        np.ndarray: A numpy array representing the buffer's data, or a tuple of arrays for certain formats.
    """
    # Map the buffer to access data
    success, map_info = buffer.map(Gst.MapFlags.READ)
    if not success:
        raise ValueError("Buffer mapping failed")

    try:
        # Handle different formats based on the provided format parameter
        handler = FORMAT_HANDLERS.get(format)
        if handler is None:
            raise ValueError(f"Unsupported format: {format}")
        return handler(map_info, width, height)
    finally:
        buffer.unmap(map_info)


# ---------------------------------------------------------
# Useful functions for working with GStreamer
# ---------------------------------------------------------

def disable_qos(pipeline):
    """
    Iterate through all elements in the given GStreamer pipeline and set the qos property to False
    where applicable.
    When the 'qos' property is set to True, the element will measure the time it takes to process each buffer and will drop frames if latency is too high.
    We are running on long pipelines, so we want to disable this feature to avoid dropping frames.
    :param pipeline: A GStreamer pipeline object
    """
    # Ensure the pipeline is a Gst.Pipeline instance
    if not isinstance(pipeline, Gst.Pipeline):
        print("The provided object is not a GStreamer Pipeline")
        return

    # Iterate through all elements in the pipeline
    it = pipeline.iterate_elements()
    while True:
        result, element = it.next()
        if result != Gst.IteratorResult.OK:
            break

        # Check if the element has the 'qos' property
        if 'qos' in GObject.list_properties(element):
            # Set the 'qos' property to False
            element.set_property('qos', False)
            print(f"Set qos to False for {element.get_name()}")
