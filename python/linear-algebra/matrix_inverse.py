
"""Compute matrix inverse module."""

import copy

import numpy as np


def inverse(x):
    size_n = len(x)
    x1 = copy.deepcopy(x)
    e1 = np.eye(size_n)

    for idx in range(size_n):
        for i in range(idx):
            f = x1[idx][i] / x1[i][i]
            for j in range(size_n):
                x1[idx][j] -= f * x1[i][j]
                e1[idx][j] -= f * e1[i][j]

        if not any(x1[idx]):
            raise ValueError("non inverted matrix.")

        f = x1[idx][idx]
        for i in range(size_n):
            x1[idx][i] /= f
            e1[idx][i] /= f

    for idx in range(size_n - 1, -1, -1):
        for i in range(size_n - 1, idx, -1):
            f = x1[idx][i] / x1[i][i]
            for j in range(len(x)):
                x1[idx][j] -= f * x1[i][j]
                e1[idx][j] -= f * e1[i][j]

        if not any(x1[idx]):
            raise ValueError("non inverted matrix.")

        f = x1[idx][idx]
        for i in range(size_n):
            x1[idx][i] /= f
            e1[idx][i] /= f

    return e1


def check_matrix(x1, x2):
    size_n1 = len(x1)
    size_n2 = len(x2)

    if size_n1 != size_n2:
        return False

    for i in range(size_n1):
        for j in range(size_n1):
            if abs(x1[i][j] - x2[i][j]) > 1e-8:
                return False

    return True


def main():
    size_n = np.random.randint(3, 10)
    x = list(list(np.random.randint(3, 20) for j in range(size_n)) for i in range(size_n))
    print('sample matrix size n', size_n)
    print('sample matrix det', np.linalg.det(x))

    inv_x1 = np.linalg.inv(x)
    inv_x2 = inverse(x)

    assert check_matrix(inv_x1, inv_x2), 'wrong inverted result.'


if __name__ == '__main__':
    main()
