
"""Monty hall problem simulation module."""

import random
import sys


def main():
    test_num = 1000
    if len(sys.argv) > 1:
        test_num = int(sys.argv[1])

    switch_wins = 0
    non_switch_wins = 0

    for i in range(test_num):
        sample_num = 3
        sample_space = [0] * sample_num

        idx_set = set(range(sample_num))
        gift_idx = random.randint(0, sample_num - 1)
        sample_space[gift_idx] = 1

        first_select_idx = random.randint(0, sample_num - 1)
        if sample_space[first_select_idx] == 1:
            open_idx = random.choice(tuple(idx_set - {first_select_idx}))
        else:
            open_idx = tuple(idx_set - {gift_idx, first_select_idx})[0]

        if sample_space[first_select_idx] == 1:
            # don't switch
            non_switch_wins += 1
        else:
            # switch
            second_select_idx = tuple(idx_set - {first_select_idx, open_idx})[0]
            if sample_space[second_select_idx] == 1:
                switch_wins += 1

    print(switch_wins / test_num, non_switch_wins / test_num)


if __name__ == '__main__':
    main()
