
"""Simulate main interpreter thread exiting behaviour."""

import threading
import time


class FooThread(threading.Thread):

    def join(self, timeout=None):
        print('join foo thread.', flush=True)
        super(FooThread, self).join(timeout=timeout)


def foo_job():
    print('running foo job...', flush=True)
    time.sleep(10)


def main():
    foo_thread = FooThread(target=foo_job)
    foo_thread.start()


if __name__ == '__main__':
    main()
