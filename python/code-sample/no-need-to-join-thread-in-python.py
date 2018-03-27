
"""A script to check how Python interpreter exits."""

import threading
import time


def task_handler(duration):
    time.sleep(duration)
    print('task done.')


def main():
    task = threading.Thread(target=task_handler, args=(10,))
    task.start()

    print('waiting...')


if __name__ == '__main__':
    main()
