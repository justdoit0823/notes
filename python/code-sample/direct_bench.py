import perf


class A:

    x = 1231


def direct_call(a_obj):
    return a_obj.x * 2


def main():
    runner = perf.Runner()
    runner.bench_func('run direct benchmark', direct_call, A)


if __name__ == '__main__':
    main()