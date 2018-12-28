
"""Calculate standard deviation iteratively."""

import sys
import threading

import numpy as np


_VERBOSE = False


def cal_mean2std(m, x_mean, x_std, n, y_mean, y_std):
    z_mean = (m * x_mean + n * y_mean) / (m + n)
    x_square_sum = (x_std ** 2) * m + m * (x_mean ** 2)
    y_square_sum = (y_std ** 2) * n + n * (y_mean ** 2)
    z_square_sum = x_square_sum + y_square_sum

    z_variance = z_square_sum - 2 * (m * x_mean + n * y_mean) * z_mean \
        + (m + n) * (z_mean ** 2)
    z_std = np.sqrt(z_variance / (m + n))

    return z_mean, z_std


def validate_cal_std():
    m, n = tuple(np.random.randint(1000000, 1500000) for i in range(2))

    x = 2 * np.random.random_sample(m) + 1.41
    y = 1.8 * np.random.random_sample(n) + 1.79

    x_mean, x_std = x.mean(), x.std()
    y_mean, y_std = y.mean(), y.std()
    if _VERBOSE:
        print('mean', x_mean, y_mean)
        print('std', x_std, y_std)

    z_mean, z_std = cal_mean2std(m, x_mean, x_std, n, y_mean, y_std)
    ok_z_mean = np.concatenate((x, y)).mean()
    ok_z_std = np.concatenate((x, y)).std()
    if _VERBOSE:
        print('mean', ok_z_mean, z_mean)
        print('std', ok_z_std, z_std)

    assert np.abs(z_mean - ok_z_mean) < 1e-10
    assert np.abs(z_std - ok_z_std) < 1e-10


def main():
    if len(sys.argv) < 2:
        print('test num is missing.')
        return

    n = int(sys.argv[1])
    n_thread = 1
    if len(sys.argv) > 2:
        n_thread = int(sys.argv[2])

    def run_task(n):
        for i in range(n):
            validate_cal_std()

    thread_list = tuple(
        threading.Thread(target=run_task, args=(n // n_thread,))
        for i in range(n_thread))
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print('done.')


if __name__ == '__main__':
    main()
