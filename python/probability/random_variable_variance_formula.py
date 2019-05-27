
"""Random variable variance formula module."""

import numpy as np


def diff_variance(x):
    e = np.mean(x)
    v = np.var(x)
    v1 = np.mean(x ** 2) - np.mean(x) ** 2

    return np.abs(v - v1)


def check_single_variable():
    rounds = [10, 100, 1000, 10000, 100000, 1000000]
    print('begin checking single variable.')
    for n in rounds:
        x = np.random.random_sample(n)
        diff = diff_variance(x)
        print(f'round {n} diff:{diff}.')

    print('finish checking single variable.')


def check_multi_variable():
    rounds = [10, 100, 1000, 10000, 100000, 1000000]
    print('begin checking multi variable.')
    for n in rounds:
        x = np.random.random_sample(n)
        y = 5 * np.random.random_sample(n) + 1
        diff = diff_variance(x + y)
        print(f'round {n} diff:{diff}.')

    print('finish checking multi variable.')


def main():
    check_single_variable()
    print('')
    check_multi_variable()


if __name__ == '__main__':
    main()
