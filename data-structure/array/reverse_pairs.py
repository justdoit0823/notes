
"""Reverse pairs within an array."""


def reverse_pairs(a_list):
    r_pairs = []

    for idx, val in enumerate(a_list):
        if idx == 0 or val > a_list[idx - 1]:
            r_pairs.append([])
            r_pairs[-1].append(val)
        elif val <= a_list[idx - 1]:
            r_pairs[-1].append(val)

    return r_pairs


def main():
    a_list = [5, 4, 3, 2, 1, 3, 2, 4, 5, 6, 5, 4]
    assert reverse_pairs(a_list) == [[5, 4, 3, 2, 1], [3, 2], [4], [5], [6, 5, 4]]


if __name__ == '__main__':
    main()
