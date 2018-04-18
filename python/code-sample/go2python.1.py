
import queue
import threading

w_queue = queue.Queue(maxsize=10)


def foo():
    print(w_queue.get())


def main():
    f_worker = threading.Thread(target=foo)
    f_worker.start()

    w_queue.put('Hello, world')


if __name__ == '__main__':
    main()
