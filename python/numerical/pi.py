
"""Calculate const pi."""

import sys
import time

import numpy as np


def calculate_pi(n):
    np.random.seed(int(time.time()))
    x = np.random.random(n)
    y = np.random.random(n)

    points = np.stack([x, y], axis=1)
    return ((points[:, :2] ** 2).sum(axis=1) <= 1).sum() / n * 4


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
    print(f'calculated pi is {calculate_pi(n)}')


if __name__ == '__main__':
    main()
