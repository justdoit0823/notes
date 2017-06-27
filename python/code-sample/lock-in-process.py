
import multiprocessing
import os
import threading
import time

import click


@click.group()
def main():
    pass


def child_thread(lock):
    with lock:
        time.sleep(20)

    print('work done.')


def child_worker(lock):
    print('run child worker..')
    with lock:
        print('got lock...')

    print('child worker exit.')


@main.command('fork')
def run_fork():
    lock = threading.Lock()
    child_t = threading.Thread(target=child_thread, args=(lock,))
    child_t.start()
    print('main thread identity', threading.get_ident())
    pid = os.fork()
    if pid == -1:
        raise RuntimeError('fork failed.')

    if pid == 0:
        print('main thread identity', threading.get_ident())
        child_worker(lock)
    else:
        time.sleep(120)


@main.command('popen')
def run_popen():
    lock = threading.Lock()
    child_t = threading.Thread(target=child_thread, args=(lock,))
    child_t.start()

    child_p = multiprocessing.Process(target=child_worker, args=(lock,))
    child_p.start()
    child_p.join(timeout=120)


if __name__ == '__main__':
    main()
