import time
from abc import ABCMeta, abstractmethod
from random import random


class BackoffTimer:
    __metaclass__ = ABCMeta

    def __init__(self, maximum=10, timeout=300, jitter=0.1):
        self.maximium = maximum
        self.jitter = jitter
        self.timeout = timeout

        self.start_time = time.time()
        self.ticks = 0

    def __iter__(self):
        return self

    def next(self):
        elapsed = time.time() - self.start_time
        if elapsed >= self.timeout:
            raise StopIteration("Timeout", elapsed)

        sleep_time = min(self.next_value(), self.maximium)
        sleep_time += random() * self.jitter
        time.sleep(sleep_time)
        self.ticks += 1
        return sleep_time

    @abstractmethod
    def next_value(self):
        pass


class FibonacciTimer(BackoffTimer):

    def __init__(self, start_with=1, maximum=10, timeout=300, jitter=0.1):
        BackoffTimer.__init__(self, maximum, timeout, jitter)
        self.ticks = start_with

    def next_value(self):
        return FibonacciTimer.fibonacci(self.ticks)

    @staticmethod
    def fibonacci(n):
        if n == 0:
            return 0

        a, b = 1, 1
        for i in range(n-1):
            a, b = b, a + b
        return a


class LinearTimer(BackoffTimer):

    def __init__(self, slope=2.0, intercept=0.0, maximum=10, timeout=300, jitter=0.1):
        BackoffTimer.__init__(self, maximum, timeout, jitter)
        self.slope = slope
        self.intercept = intercept

    def next_value(self):
        return self.ticks * self.slope + self.intercept


class TimerTimeoutError(Exception):
    pass


timer = FibonacciTimer(start_with=2, timeout=5, jitter=0)
# timer = LinearTimer(slope=0.25, intercept=0.25, timeout=5, jitter=0)

while True:
    pass

    try:
        tick_time = timer.next()
        print "waited", tick_time, "seconds"
    except StopIteration as e:
        message, tick_time = e.args
        print "timed out after", tick_time, "seconds"
        exit(1)
