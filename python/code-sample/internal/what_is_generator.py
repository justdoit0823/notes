# -*- coding: utf-8 -*-

'''
This is a module for testing generator usage.

'''


def simple_number_generator(n):

    '''
    A simple number generator.

    '''

    for i in range(n):

        yield i


def test_simple_number_generator():

    x = simple_number_generator(5)

    print simple_number_generator, x

    try:

        while True:

            num = next(x)

            print num

    except StopIteration, e:

        print e


def main():

    test_simple_number_generator()


if __name__ == '__main__':

    main()
