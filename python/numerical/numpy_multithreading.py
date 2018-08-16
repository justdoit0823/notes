
"""test numpy multhreading support module."""

import threading
import time

import numpy as np


def compute_task(m, n):
    for i in range(m):
        x = np.linspace(1, 100, num=n)
        y = np.linspace(200, 400, num=n)
        x.dot(y.reshape(-1, 1))


def main():
    ts_no_thread_start = time.time()
    for i in range(10):
        compute_task(1000, 10000)

    ts_no_thread_end = time.time()
    print('no thread running time', ts_no_thread_end - ts_no_thread_start)

    ts_thread_start = time.time()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=compute_task, args=(1000, 10000))
        thread.start()

    for thread in threads:
        Thread.join()

    ts_thread_end = time.time()
    print('thread running time', ts_thread_end - ts_thread_start)


if __name__ == '__main__':
    main()
