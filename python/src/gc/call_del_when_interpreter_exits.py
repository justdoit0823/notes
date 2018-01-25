
"""Check whether __del__ function is called when the interpreter exits."""

import gc
import threading
import time


class ResourceObject:

    def __init__(self, seq, scope):
        self.seq = seq
        self.scope = scope

    def __str__(self):
        return '{0}<{1}><{2}>.{3}'.format(
            self.__class__.__name__, hex(id(self)), self.scope, self.seq)

    def __del__(self):
        print('do finalization of object %s.' % self, flush=True)


def run_with_resource(seq):
    res = ResourceObject(seq, 'local-variable')
    print(res, flush=True)


def run_in_thread(seq, timeout):
    run_with_resource(seq)
    time.sleep(timeout)
    print('thread exits.', flush=True)


def run_with_resource_in_thread(res, timeout):
    print(res, flush=True)
    time.sleep(timeout)


global_res = ResourceObject(3000000, 'global-variable')


def run_with_global_resource_in_thread(timeout):
    print(global_res, flush=True)
    time.sleep(timeout)


def main():

    # Disbale garbage collection
    gc.disable()

    # Finalize local variable
    run_with_resource(123)

    thread1 = threading.Thread(target=run_in_thread, args=(111111, 10))
    thread1.start()

    # Finalize bypass local variable
    res2 = ResourceObject(222233333, 'bypass-local-variable')
    thread2 = threading.Thread(target=run_with_resource_in_thread, args=(res2, 5))
    thread2.start()

    # Finalize global variable
    thread3 = threading.Thread(
        target=run_with_global_resource_in_thread, args=(6,))
    thread3.start()

    thread2.join()
    print('thread2 exits.')


if __name__ == '__main__':
    main()
