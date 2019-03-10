
"""Reflection image."""

import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import load_sample_image


def reflect_sample():
    china = load_sample_image('china.jpg')
    print('the original china image.')
    plt.imshow(china)
    plt.show()

    n_row, n_col, n_dim = china.shape
    m_reflect = np.zeros((n_row, n_row), dtype=int)

    for i in range(n_row):
        m_reflect[i, n_row - 1 - i] = 1

    new_china = np.stack(tuple(m_reflect.dot(china[:, :, d]) for d in range(n_dim)), axis=-1)
    print('the reflected china image.')
    plt.imshow(new_china)
    plt.show()


if __name__ == '__main__':
    reflect_sample()
