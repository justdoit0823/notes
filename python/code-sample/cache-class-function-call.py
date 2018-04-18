
import time

import click



class AClass:

    @classmethod
    def sum(cls, i_max):
        r_sum = 0
        for i in range(i_max // 2):
            r_sum += 1 + i_max

        return r_sum
        # return (1 + i_max) * i_max / 2


@click.group()
def main():
    pass


@main.command('test', help='run benchmark')
@click.argument('loop', type=int, default=10000)
@click.argument('count', type=int, default=10)
@click.argument('cache', type=int, default=0)
def test(**kwargs):

    if kwargs['cache']:
        setattr(AClass, 'sum', AClass.sum)

    benchmark_times = []
    for count_i in range(kwargs['count']):
        start_time = time.time()
        for i in range(kwargs['loop']):
            AClass.sum(i)
        end_time = time.time()

        benchmark_times.append(end_time - start_time)

    print('run {0} benchmark, max time {1}, min time {2}, avg time {3}'.format(
        kwargs['loop'], max(benchmark_times), min(benchmark_times),
        sum(benchmark_times) / len(benchmark_times)))


if __name__ == '__main__':

    main()
