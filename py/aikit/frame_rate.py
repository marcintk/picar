from time import time
from typing import Tuple

_SEC: int = 1


class FrameRate:
    class _Prober(object):
        def __init__(self) -> None:
            self._counter: int = 0
            self._start_time = time()

        def probe(self) -> Tuple[bool, float]:
            elapsed = self._elapsed()
            rate = self._counter / elapsed

            self._counter += 1
            return True, rate

        def _elapsed(self) -> float:
            return time() - self._start_time

    class _IntervalProber(_Prober):
        def __init__(self, interval: int) -> None:
            super().__init__()
            self._interval = interval
            self._last: float = 0.0

        def probe(self) -> Tuple[bool, float]:
            elapsed: float = self._elapsed()
            recalculate: bool = elapsed > self._interval

            if recalculate:
                self._last = self._counter / elapsed
                self._counter = 0
                self._start_time = time()
            else:
                self._counter += 1

            return recalculate, self._last

    def __init__(self) -> None:
        self._last_rate: FrameRate._IntervalProber = FrameRate._IntervalProber(_SEC)
        self._rate: FrameRate._Prober = FrameRate._Prober()

    def probe(self) -> Tuple[float, bool, float]:
        probe: Tuple[bool, float] = self._last_rate.probe()
        return self._rate.probe()[1], probe[0], probe[1]
