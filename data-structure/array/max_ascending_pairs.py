
"""Max ascending pairs."""


def max_ascending_pairs(a_list):
    m_low_idx = None
    m_high_idx = None
    c_low_idx = None
    c_high_idx = None

    for idx, val in enumerate(a_list):
        if idx == 0:
            c_low_idx = idx
            c_high_idx = idx
        else:
            if val >= a_list[idx - 1]:
                c_high_idx = idx
            else:
                if m_low_idx is None:
                    m_low_idx = c_low_idx
                    m_high_idx = c_high_idx
                else:
                    if (c_high_idx - c_low_idx) > (m_high_idx - m_low_idx):
                        m_low_idx = c_low_idx
                        m_high_idx = c_high_idx

                c_low_idx = idx
                c_high_idx = idx

    if (c_high_idx - c_low_idx) > (m_high_idx - m_low_idx):
        m_low_idx = c_low_idx
        m_high_idx = c_high_idx

    return a_list[m_low_idx: m_high_idx + 1]


def main():
    test_list = [1, 2, 3, 2, 3, 4, 5, 6, 5, 7, 8, 9, 10, 11]
    assert max_ascending_pairs(test_list) == [5, 7, 8, 9, 10, 11]


if __name__ == '__main__':
    main()
