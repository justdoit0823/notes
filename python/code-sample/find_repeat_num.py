
import random


def find_repeat_num(seqs):
    idx = 0
    s_len = len(seqs)
    while idx < s_len:
        num = seqs[idx]
        if idx == num - 1:
            idx += 1
            continue

        if num == seqs[num - 1]:
            return num

        seqs[num - 1], seqs[idx] = num, seqs[num - 1]


def main():
    for idx in range(1000):
        t_seq = list(range(1, 101))
        dup_idx = random.randint(0, 99)
        step = random.randint(1, 99)
        t_seq[(dup_idx + step) % 100] = t_seq[dup_idx]

        assert t_seq[dup_idx] == find_repeat_num(list(t_seq))


if __name__ == '__main__':
    main()
