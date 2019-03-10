
"""Reflection image."""

import click
import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import load_sample_image


@click.group()
def main():
    pass


@main.command('reflect')
def reflect_sample():
    china = load_sample_image('china.jpg')

    f, axes = plt.subplots(1, 2)
    axes[0].set_title('the original china image.')
    axes[0].imshow(china)

    n_row, n_col, n_dim = china.shape
    m_reflect = np.zeros((n_row, n_row), dtype=int)

    for i in range(n_row):
        m_reflect[i, n_row - 1 - i] = 1

    new_china = np.stack(tuple(m_reflect.dot(china[:, :, d]) for d in range(n_dim)), axis=-1)
    axes[1].set_title('the reflected china image.')
    axes[1].imshow(new_china)

    plt.show()


@main.command('invert')
def invert_sample():
    china = load_sample_image('china.jpg')

    f, axes = plt.subplots(1, 2)
    axes[0].set_title('the original china image.')
    axes[0].imshow(china)

    n_row, n_col, n_dim = china.shape
    m_flip = np.zeros((n_col, n_col), dtype=int)

    for i in range(n_col):
        m_flip[i, n_col - 1 - i] = 1

    new_china = np.stack(tuple(m_flip.dot(china[:, :, d].T).T for d in range(n_dim)), axis=-1)
    axes[1].set_title('the inverted china image.')
    axes[1].imshow(new_china)

    plt.show()


if __name__ == '__main__':
    main()
