
"""Bisection search module."""


def bisection_search(x, i_list):
    low = 0
    high = len(i_list) - 1

    while low <= high:
        median = (low + high) // 2
        if x == i_list[median]:
            return median
        elif x > i_list[median]:
            low = median + 1
        else:
            high = median - 1

    return -1


def bisection_search_left(x, i_list):
    low = 0
    high = len(i_list) - 1

    while low <= high:
        median = (low + high) // 2
        if x == i_list[median]:
            if median == low or i_list[median - 1] < x:
                return median

            high = median - 1
        elif x > i_list[median]:
            low = median + 1
        else:
            high = median - 1

    return -1


def bisection_search_right(x, i_list):
    low = 0
    high = len(i_list) - 1

    while low <= high:
        median = (low + high) // 2
        if x == i_list[median]:
            if median == high or i_list[median + 1] > x:
                return median

            low = median + 1
        elif x > i_list[median]:
            low = median + 1
        else:
            high = median - 1

    return -1


def main():
    x1 = [1, 3, 4, 5, 5, 5, 7, 10]
    assert bisection_search(5, x1) >= 3
    assert bisection_search_left(5, x1) == 3
    assert bisection_search_right(5, x1) == 5

    x2 = [1, 1, 3, 5, 8, 10, 12]
    assert bisection_search(3, x2) == 2
    assert bisection_search_left(1, x2) == 0

    x3 = [3, 6, 8, 10, 12, 15, 15, 15]
    assert bisection_search_right(15, x3) == 7


if __name__ == '__main__':
    main()
