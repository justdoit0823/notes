
"""Gram-Schmidt process."""

import numpy as np


def projection(x, y):
    assert x.size == y.size, "x and y dimension must be equal."

    dot_p = x.dot(y)
    factor = dot_p / x.dot(x)

    return factor * x


def norm(x):
    len_x = np.sqrt(x.dot(x))
    return x / len_x


def gram_schmidt(x, e_list):
    next_dim_idx = len(e_list)
    u = x[next_dim_idx, :]

    for i in range(next_dim_idx):
        u -= projection(e_list[i], u)

    return norm(u)


def main():
    size_n = np.random.randint(3, 10)
    x = np.random.rand(size_n, size_n)
    print(x)

    e_list = []
    for i in range(size_n):
        e_list.append(gram_schmidt(x, e_list))

    e = np.array(e_list)
    print(np.round(np.dot(e, e.T), 2), np.linalg.det(e))


if __name__ == '__main__':
    main()
