
"""Shunting yard algorithm."""

from collections import deque


def transfer(in_str):
    out_q = deque()
    op_q = deque()

    for i_chr in in_str:
        if i_chr in ('+', '-', '*', '/'):
            if i_chr in ('+', '-'):
                while op_q:
                    if op_q[-1] in ('*', '/', '+', '-'):
                        o_chr = op_q.pop()
                        out_q.append(o_chr)
                    else:
                        break
            else:
                while op_q:
                    if op_q[-1] in ('*', '/'):
                        o_chr = op_q.pop()
                        out_q.append(o_chr)
                    else:
                        break

            op_q.append(i_chr)
        else:
            out_q.append(i_chr)

    while op_q:
        out_q.append(op_q.pop())

    return ''.join(map(str, out_q))


def main():
    input_str = 'a+b*c+d+f/e'
    assert transfer(input_str) == 'abc*+d+fe/+'

    input_str = 'a-b+c*d/e+f-g'
    assert transfer(input_str) == 'ab-cd*e/+f+g-'


if __name__ == '__main__':
    main()
