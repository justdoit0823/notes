
import queue
import threading

w_queue = queue.Queue(maxsize=10)


def foo():
    w_queue.put('Hello, world')

    
def main():
    f_worker = threading.Thread(target=foo)
    f_worker.start()
    print(w_queue.get())


if __name__ == '__main__':
    main()
