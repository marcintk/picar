import multiprocessing


class HailoData:
    def __init__(self):
        self.frame_queue = multiprocessing.Queue(maxsize=3)  # set up a multiprocessing queue to pass the frame to the main thread
        self.frame_count = 0
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
