
"""Multithreading sum script."""

import sys
import threading


def sum_task(idx, n_start, n_stop, ret):
    total = 0
    while n_start < n_stop:
        total += n_start
        n_start += 1

    ret[idx] = total


def main():
    num = int(sys.argv[1])
    thread_num = int(sys.argv[2])

    ret = [0] * thread_num
    size = num // thread_num
    threads = []

    for idx in range(thread_num):
        n_start = idx * size
        if idx == thread_num - 1:
            n_stop = num
        else:
            n_stop = n_start + size

        thread = threading.Thread(
            target=sum_task, args=(idx, n_start, n_stop, ret))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print('sum %d.' % sum(ret))


if __name__ == '__main__':
    main()
