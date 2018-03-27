
"""An example program about how to use periodic callback in tornado."""


import time

from tornado.ioloop import IOLoop, PeriodicCallback


def test_callback():
    print('run callback', time.time())


def main():
    pcb = PeriodicCallback(test_callback, 15 * 1000)
    pcb.start()
    IOLoop.instance().start()


if __name__ == '__main__':
    main()
