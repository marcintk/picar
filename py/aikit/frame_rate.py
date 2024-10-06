from time import time

_SEC: int = 1


class FrameRate:
    class _Prober(object):
        def __init__(self):
            self._counter: int = 0
            self._start_time = time()

        def probe(self) -> float:
            elapsed = self._elapsed()
            rate = self._counter / elapsed

            self._counter += 1
            return rate

        def _elapsed(self) -> float:
            return time() - self._start_time

    class _IntervalProber(_Prober):
        def __init__(self, interval: int):
            super().__init__()
            self._interval = interval
            self._last: float = 0.0

        def probe(self) -> (bool, float):
            elapsed: float = self._elapsed()
            recalculate: bool = elapsed > self._interval

            if recalculate:
                self._last = self._counter / elapsed
                self._counter = 0
                self._start_time = time()
            else:
                self._counter += 1

            return recalculate, self._last

    def __init__(self):
        self._last_rate: FrameRate._IntervalProber = FrameRate._IntervalProber(_SEC)
        self._rate: FrameRate._Prober = FrameRate._Prober()

    def probe(self) -> (float, bool, float):
        return self._rate.probe(), *self._last_rate.probe()
