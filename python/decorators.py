# -*- coding: utf-8 -*-

'''
This is a file to show how python decorator does.

'''


def show_name2address(v):

    '''
    show the instance information about name and memory address

    '''

    print '%s %s and address 0x%x' % (type(v).__name__,
                                      getattr(v, '__name__', ''), id(v))


def no_argument_decorator():

    '''
    function decorator with one arguments.
    Usage example
    >>> @one_argument_decorator()
    >>> def your_function(*args):
    >>>     write your own code
    '''

    def wrap(fun):

        show_name2address(fun)

        def innerwrap(*args):

            print 'execute in innerwrap'

            return fun(*args)

        show_name2address(innerwrap)

        return innerwrap

    show_name2address(wrap)

    return wrap


@no_argument_decorator()
def test_no_argument_decorator(*args):

    print 'execute in test_no_argument_decorator'

    print args


show_name2address(test_no_argument_decorator)

test_no_argument_decorator(*[1, 'justdoit', 'programer'])


try:

    @no_argument_decorator
    def test_no_explicit_argument_decorator(*args):

        print 'execute in test_no_explicit_argument_decorator'

        print args
except Exception, e:

    print e


def one_argument_decorator(fun):

    '''
    function decorator with one arguments.
    Usage example
    >>> @one_argument_decorator(default=below funtion)
    >>> def your_function(*args):
    >>>     write your own code
    '''

    show_name2address(fun)

    def wrap(*args):

        print args

        return fun(*args)

    return wrap

try:

    @one_argument_decorator
    def test_one_argument_decorator(x):

        return x**2
except Exception, e:

    print e

print test_one_argument_decorator(3)


try:

    @one_argument_decorator()
    def test_one_explicitno_argument_decorator(x):

        return 2*x
except Exception, e:

    print e


def two_arguments_decorator(fun, arg):

    '''
    function decorator with two arguments.
    Usage example
    >>> @two_arguments_decorator(fun, arg)
    >>> def your_function(*args):
    >>>     write your own code
    '''
    show_name2address(fun)

    show_name2address(arg)

    def wrap(func):

        show_name2address(func)

        def innerwrap(*args):

            return func(args)

        show_name2address(innerwrap)

        return innerwrap

    show_name2address(wrap)

    return wrap

try:

    @two_arguments_decorator(123, 'abc')
    def test_two_arguments_decorator(s):

        print s

except Exception, e:

    print e

print test_two_arguments_decorator('def')
