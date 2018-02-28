
"""Dichotomy search algorithm."""

def bisect_search(s_list, val):
    low = 0
    high = len(s_list) - 1

    while low <= high:
        middle = (low + high) // 2
        middle_val = s_list[middle]
        if middle_val == val:
            return middle
        elif middle_val < val:
            low = middle + 1
        else:
            high = high - 1

    return -1


def main():
    test_list = range(0, 20, 2)

    assert bisect_search(test_list, 1) == -1
    assert bisect_search(test_list, 23) == -1

    assert bisect_search(test_list, 10) == 5
    assert bisect_search(test_list, 16) == 8


if __name__ == '__main__':
    main()
