
"""Check whether __del__ function is called when the interpreter exits.

Called when the instance is about to be destroyed. This is also called a finalizer or (improperly) a destructor.
If a base class has a __del__() method, the derived class’s __del__() method,
if any, must explicitly call it to ensure proper deletion of the base class part of the instance.

It is possible (though not recommended!) for the __del__() method to postpone destruction of the instance by creating a new reference to it.
This is called object resurrection. It is implementation-dependent whether __del__() is called a second time when a resurrected object is about to be destroyed; the current CPython implementation only calls it once.

It is not guaranteed that __del__() methods are called for objects that still exist when the interpreter exits.
`del x` doesn’t directly call x.__del__() — the former decrements the reference count for x by one,
and the latter is only called when x’s reference count reaches zero.
"""

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


def run_with_resource_as_closure(seq):
    res = ResourceObject(seq, 'closure-variable')

    def bar():
        print(res, flush=True)

    print(res, flush=True)

    return bar


def run_in_thread(seq, timeout):
    res = ResourceObject(seq, 'local-variable-in-thread')
    print('access local resource', res, 'in thread', flush=True)

    time.sleep(timeout)
    print('thread exits.', flush=True)


def run_with_resource_in_thread(res, timeout):
    print('access bypass resource', res, 'in thread', flush=True)

    time.sleep(timeout)
    print('thread with bypass resource exits.')


global_res = ResourceObject(3000000, 'global-variable')


def run_with_global_resource_in_thread(timeout):
    print('access global resource', global_res, 'in thread', flush=True)

    time.sleep(timeout)
    print('thread with global resource exits.')


def main():

    # Disbale garbage collection
    gc.disable()

    print('start to detect when method `__del__` will be called.\n')

    # Finalize local variable
    run_with_resource(123)

    print('')

    # Finalize closure variable
    run_with_resource_as_closure(123456)

    print('')

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

    print('\nwaiting...\n')


if __name__ == '__main__':
    main()
