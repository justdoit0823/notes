
import click
import time


@click.group()
def main():
    pass


class A:

    x = 1231


def direct_call(a_obj):
    return a_obj.x * 2


def indirect_call(a_obj):
    x = a_obj.x
    return x * 2


@main.command('run')
@click.argument('direct', type=int, default=0)
@click.argument('loop', type=int, default=100)
@click.argument('count', type=int, default=10000)
def run(**kwargs):
    direct = kwargs['direct']
    loop = kwargs['loop']
    count = kwargs['count']

    if direct:
        run_direct_reference(loop, count)
    else:
        run_indirect_reference(loop, count)


def benchmark(loop, count, func, time_func):
    t_s_time = time_func()
    durations = []
    for idx in range(loop):
        s_time = time_func()

        for c_idx in range(count):
            func(A)

        e_time = time_func()
        durations.append(e_time - s_time)

    t_e_time = time_func()
    print(
        'test {0} loops and iterate count {1}, max time {2}s, avg time {3}s, '
        'min time {4}s, total run time {5}s'.format(
            loop, count, max(durations), sum(durations) / loop, min(durations),
            (t_e_time - t_s_time)))


def run_direct_reference(loop, count):
    benchmark(loop, count, direct_call, time.monotonic)


def run_indirect_reference(loop, count):
    benchmark(loop, count, indirect_call, time.monotonic)


if __name__ == '__main__':
    main()
