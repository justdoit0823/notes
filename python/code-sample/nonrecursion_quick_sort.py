
"""非递归quick sort."""

import random
import sys


def partition(s, low, high):
    """切分函数."""
    if low == high:
        return low

    pivot = (low + high) // 2
    pivot_value = s[pivot]
    low_idx = low
    s[pivot], s[high] = s[high], pivot_value
    for idx in range(low, high):
        if s[idx] <= pivot_value:
            if idx > low_idx:
                s[low_idx], s[idx] = s[idx], s[low_idx]

            low_idx += 1

    s[low_idx], s[high] = pivot_value, s[low_idx]
    return low_idx


def quick_sort(s_list):
    """非递归版quick sort."""
    low = 0
    high = len(s_list) - 1
    sort_partitions = {(low, high)}
    while sort_partitions:
        par_low, par_high = sort_partitions.pop()
        pivot = partition(s_list, par_low, par_high)
        if pivot > par_low:
            sort_partitions.add((par_low, pivot - 1))
        if pivot < par_high:
            sort_partitions.add((pivot + 1, par_high))


def main():
    """执行主入口."""
    if len(sys.argv) == 1:
        test_num = 10000
    else:
        test_num = int(sys.argv[1])

    test_list = [random.randint(0, 10000) for i in range(test_num)]
    print(test_list)
    quick_sort(test_list)
    print(test_list)


if __name__ == '__main__':
    main()
