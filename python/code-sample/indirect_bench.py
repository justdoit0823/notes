
import perf


class A:

    x = 1231


def indirect_call(a_obj):
    x = a_obj.x
    return x * 2


def main():
    runner = perf.Runner()
    runner.bench_func('run indirect benchmark', indirect_call, A)


if __name__ == '__main__':
    main()