
"""Check sequence."""

import sys


def check_chunck_seq(i_tuple, size):
    for idx, val in enumerate(i_tuple):
        if idx % size == 0:
            continue

        if val != i_tuple[idx - 1] + 1:
            raise ValueError('inconsistent sequence.')


def main():
    size = 10
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    output = sys.stdin.read()
    i_tuple = tuple(map(int, output[1: -2].split(',')))

    try:
        check_chunck_seq(i_tuple, 10)
    except ValueError:
        print("thread switch.")


if __name__ == '__main__':
    main()
