# -*- coding: utf-8 -*-

'''
This is a file to show how python decorator does.

Normaly, we use the python decorator like this:

@a_callable_object
def your_method(*args):
    do_something

@a_callable_object
class your_class():
    define_your_class

And the callable object can be a funtion, class object.

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
    >>> @no_argument_decorator()
    >>> def your_function(*args):
    >>>     write your own code
    At this time, you can't use as @no_argument_decorator,
    because your decorator function has no argument and
    decorator must callback with your_function as an argument.
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


try:

    '''
    test no_argument_decorator with no argument for function

    '''

    @no_argument_decorator()
    def test_no_argument_decorator(*args):

        print 'execute in test_no_argument_decorator'

        print args

except Exception, e:

    print e
# The name and address of test_no_argument_decorator function has been changed

show_name2address(test_no_argument_decorator)
# really, perform as invoking innerwrap functio
test_no_argument_decorator(*[1, 'justdoit', 'programer'])


try:

    '''
    test no_argument_decorator with no argument for class

    '''

    @no_argument_decorator()
    class test_no_argument_decorator_class():

        def __init__(self, *args):

            print 'init in test_no_argument_decorator_class'

            print args
except Exception, e:

    print e

show_name2address(test_no_argument_decorator_class)

test_no = test_no_argument_decorator_class(*(1, 2, 3))

show_name2address(test_no)


try:

    @no_argument_decorator
    def test_no_explicit_argument_decorator(*args):

        print 'execute in test_no_explicit_argument_decorator'

        print args
except Exception, e:

    print e


def single_argument_decorator(fun):

    '''
    function decorator with one single arguments.
    Usage example
    >>> @single_argument_decorator(default=below funtion)
    >>> def your_function(*args):
    >>>     write your own code
    '''

    show_name2address(fun)

    def wrap(*args):

        print args

        return fun(*args)

    return wrap

try:

    @single_argument_decorator
    def test_single_argument_decorator(x):

        return x**2
except Exception, e:

    print e

print test_single_argument_decorator(3)


try:

    @single_argument_decorator()
    def test_one_explicitno_argument_decorator(x):

        return 2*x
except Exception, e:

    print e


def multi_arguments_decorator(fun, arg):

    '''
    function decorator with multi arguments.
    Usage example
    >>> @multi_arguments_decorator(fun, arg)
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

    @multi_arguments_decorator(123, 'abc')
    def test_multi_arguments_decorator(s):

        print s

except Exception, e:

    print e

print test_multi_arguments_decorator('def')


class no_argument_class_decorator(object):

    '''
    This is a decorator class without argument.
    A example for usage:
    >>> @no_argument_class_decorator
    >>> def your_function(*args):
    >>>     write your own code

    '''

    def __init__(self):

        print 'in the no_argument_class_decorator init'

    def __new__(cls, fun):

        print 'in the no_argument_class_decorator new'

        show_name2address(fun)

        def wrap(*args):

            print args

            print fun(args)

        show_name2address(wrap)

        return wrap

try:

    '''
    test function with no_argument_class_decorator.

    '''

    @no_argument_class_decorator
    def test_no_argument_class_decorator(s):

        return [x[:-2] for x in s]

except Exception, e:

    print 'class decorator error'

    print e

show_name2address(test_no_argument_class_decorator)

test_no_argument_class_decorator(*('justdoit', 'basketball player'))


def property_decorator(fun, *args):

    '''
    A property decorator for class object.
    Usage for example:
    >>> class A():
    >>> @property_decorator
    >>>     def class_fun(self):
    >>>         return 'class function'

    '''

    print 'execute in property decorator'

    print fun, dir(fun), fun.func_globals, args

    return fun(fun.im_self)


class property_decorator_class(object):

    '''
    A class property decorator for class object.
    When it inherits from object, it may be decorated as a descriptor.
    In general, a descriptor is an object attribute with "binding behavior",
    one whose attribute access has been overridden by methods in the descriptor
    protocol. Those methods are __get__(), __set__(), and __delete__().If any
    of those methods are defined for an object, it is said to be a descriptor.
    see details at
    https://docs.python.org/2/howto/descriptor.html#descriptor-howto-guide
    Usage for example:
    >>> class A():
    >>> @property_decorator_class
    >>>     def class_fun(self):
    >>>         return 'class function'

    '''

    def __init__(self, fun):

        self._fun = fun

    def __get__(self, obj, type):

        print 'execute in get method'

        if obj is None:

            return self

        return self._fun(obj)

    def __set__(self, obj, value, *args):

        print 'execute in set method'

        print args

        obj.__dict__[self._fun.__name__] = value


class test_property_decorator():

    '''
    A class for testing property decorator

    '''

    def __init__(self, s):

        self._s = s

    @property_decorator_class
    def svalue(self):

        return self._s

tpd = test_property_decorator("mytest")

print test_property_decorator.svalue, tpd.svalue

tpd._s = "new mytest"

print tpd.svalue
