
"""Search substring algorithm."""


def strstr(s_total, s_sub):
    """Find the first occurrence."""
    s_idx = 0
    sub_len = len(s_sub)

    while s_idx < len(s_total) - sub_len:
        for idx, char in enumerate(s_sub):
            if s_total[s_idx + idx] != char:
                break
        else:
            return s_idx

        s_idx += 1

    return -1


def main():
    s_total = 'afewfwfwef22fefwefwfw'
    assert strstr(s_total, 'afew') == 0
    assert strstr(s_total, 'fwfw') == 4
    assert strstr(s_total, 'f22fe') == 9
    assert strstr(s_total, 'fwff') == -1
    assert strstr(s_total, '22w3') == -1


if __name__ == '__main__':
    main()
