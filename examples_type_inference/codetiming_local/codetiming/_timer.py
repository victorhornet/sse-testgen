"""Definition of Timer

See help(codetiming) for quick instructions, and
https://pypi.org/project/codetiming/ for more details.
"""

# Standard library imports
import math
import time
from contextlib import ContextDecorator
from dataclasses import dataclass, field

# Codetiming imports
from codetiming._timers import Timers


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass
class Timer(ContextDecorator):
    """Time your code using a class, context manager, or decorator"""

    timers = Timers()
    _start_time = field(default=None, init=False, repr=False)
    name = None
    text = "Elapsed time: {:0.4f} seconds"
    logger = print
    last = field(default=math.nan, init=False, repr=False)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError("Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it")

        # Calculate elapsed time
        self.last = time.perf_counter() - self._start_time
        self._start_time = None

        # Report elapsed time
        if self.logger:
            attributes = {
                "name": self.name,
                "milliseconds": self.last * 1000,
                "seconds": self.last,
                "minutes": self.last / 60,
            }
            self.logger(self.text.format(self.last, **attributes))
        if self.name:
            self.timers.add(self.name, self.last)

        return self.last

    def __enter__(self):
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info):
        """Stop the context manager timer"""
        self.stop()
