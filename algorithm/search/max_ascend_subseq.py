
"""Max ascending sub sequence."""


def max_sub_seq(x):
    index, size = 0, 1 if len(x) else 0
    max_index, max_size = 0, 1 if len(x) else 0
    for i in range(1, len(x)):
        v = x[i]

        # sub seq break
        if v < x[i - 1]:
            if size > max_size:
                max_index = index
                max_size = size

            index = i
            size = 1
        else:
            size += 1

    if size > max_size:
        max_index = index
        max_size = size

    return max_index, max_size


def main():
    x1 = []
    index1, size1 = max_sub_seq(x1)
    assert index1 == 0
    assert size1 == 0

    x2 = [1]
    index2, size2 = max_sub_seq(x2)
    assert index2 == 0
    assert size2 == 1

    x3 = range(10)
    index3, size3 = max_sub_seq(x3)
    assert index3 == 0
    assert size3 == len(x3)

    x4 = [1, 2, 3, 2, 4, 5, 6, 7, 8, 2]
    index4, size4 = max_sub_seq(x4)
    assert index4 == 3
    assert size4 == 6

    x5 = [1, 2, 3, 2, 4, 5, 4, 6, 7, 8, 10]
    index5, size5 = max_sub_seq(x5)
    assert index5 == 6
    assert size5 == 5


if __name__ == '__main__':
    main()
