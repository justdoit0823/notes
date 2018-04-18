
"""字符串搜索算法模块。"""

import sys

def common_index(string, sub_string):

    match_idx = 0
    s_probe_idx = 0
    s_substr_idx = 0
    while s_probe_idx < len(string) and s_substr_idx < len(sub_string):
        if string[s_probe_idx] == sub_string[s_substr_idx]:
            # go on matching
            s_probe_idx += 1
            s_substr_idx += 1
            if s_substr_idx == len(sub_string):
                return match_idx
        else:
            # restart matching
            match_idx += 1
            s_probe_idx = match_idx
            s_substr_idx = 0

    return -1


def kmp_index(string, sub_string):

    step_list = [1]
    sub_str_len = len(sub_string)
    for match_count in range(1, sub_str_len):
        probe_idx = 1
        begin_idx = 0
        while probe_idx + begin_idx <= match_count:
            if sub_string[begin_idx] == sub_string[begin_idx + probe_idx]:
                begin_idx += 1
            else:
                probe_idx += 1
                begin_idx = 0

        # if sub_string[match_count] == sub_string[match_count - probe_idx]:
        #     probe_idx += match_count

        step_list.append(probe_idx)

    print(step_list)
    match_idx = 0
    s_probe_idx = 0
    s_substr_idx = 0
    while s_probe_idx < len(string) and s_substr_idx < len(sub_string):
        if string[s_probe_idx] == sub_string[s_substr_idx]:
            # go on matching
            s_probe_idx += 1
            s_substr_idx += 1
            if s_substr_idx == len(sub_string):
                return match_idx
        else:
            # restart matching
            step = step_list[s_substr_idx]
            print('step', step)
            match_idx += step
            s_probe_idx = match_idx
            s_substr_idx = 0

    return -1


def real_kmp_index(string, sub_string):

    back_table = [-1, 0]
    sub_str_len = len(sub_string)
    pos = 2
    cnd = 0
    while pos < sub_str_len:
        if sub_string[pos - 1] == sub_string[cnd]:
            cnd += 1
            back_table.append(cnd)
        elif cnd > 0:
            cnd = back_table[cnd]
            continue
        else:
            back_table.append(0)

        pos += 1

    match_idx = 0
    s_probe_idx = 0
    s_substr_idx = 0
    while s_probe_idx < len(string) and s_substr_idx < len(sub_string):
        if string[s_probe_idx] == sub_string[s_substr_idx]:
            # go on matching
            s_probe_idx += 1
            s_substr_idx += 1
            if s_substr_idx == len(sub_string):
                return match_idx
        else:
            # restart matching
            step = s_substr_idx - back_table[s_substr_idx]
            print('step in real kmp', step)
            match_idx += step
            s_probe_idx = match_idx
            s_substr_idx = 0

    return -1


def main():

    string = sys.argv[1]
    sub_string = sys.argv[2]
    index = common_index(string, sub_string)
    print('find index {0} of {1} in {2}'.format(
        index, sub_string, string), string.find(sub_string),
          kmp_index(string, sub_string), real_kmp_index(string, sub_string))


if __name__ == '__main__':

    main()
