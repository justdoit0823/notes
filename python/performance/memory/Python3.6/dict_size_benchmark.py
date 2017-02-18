
# -*- coding: utf-8 -*-

"""Python字典内存benchmark模块。"""

from __future__ import print_function

import os
import sys


def test_int_key(val_size=100):

    key_num = [1, 4, 10, 50, 100, 500, 1000, 5000, 10000]
    for num in key_num:
        d = {i: os.urandom(val_size) for i in range(num)}
        print(num, sys.getsizeof(d))


def test_str_key(key_size=10, val_size=100):

    key_num = [1, 4, 10, 50, 100, 500, 1000, 5000, 10000]
    for num in key_num:
        d = {os.urandom(key_size): os.urandom(val_size) for i in range(num)}
        print(num, sys.getsizeof(d))


def test_tuple_key(key_size=10, val_size=100):

    key_num = [1, 4, 10, 50, 100, 500, 1000, 5000, 10000]
    for num in key_num:
        d = {(i,) * key_size: os.urandom(val_size) for i in range(num)}
        print(num, sys.getsizeof(d))


def main():

    print('test python version:', sys.version)

    print('-------\nstart benchmark with int key------')
    test_int_key()
    print('------end benchmark with int key-----\n')

    print('-----start benchmark with str key-----')
    test_str_key()
    print('-----end benchmark with str key-------\n')

    print('-----start benchmark with tuple key----')
    test_tuple_key()
    print('-----end benchmark with tuple key----\n')


if __name__ == '__main__':

    main()
