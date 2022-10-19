
import os
import perf
import time


class A:

    x = 1231


def direct_call(a_obj):
    return a_obj.x * 2


def indirect_call(a_obj):
    x = a_obj.x
    return x * 2


def benchmark(name, func):
    runner = perf.Runner()
    runner.timeit(name, stmt='func(A)', globals={'func': func, 'A': A})


def main():
    if os.getenv('RUN_DIRECT', '0') == '0':
        print('run indirect')
        benchmark('run indirect', indirect_call)
    else:
        print('run direct')
        benchmark('run direct', direct_call)


if __name__ == '__main__':
    main()