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

The gramar may do like this:

your_method = a_callable_object(your_method)

you_class = a_callable_object(your_class)

It will do a previous name linking to a new object.

'''


def show_name2address(v):

    '''
    show the instance information about name and memory address

    '''

    print '%s %s and address 0x%x' % (type(v).__name__,
                                      getattr(v, '__name__', ''), id(v))


def test_case(test_fun):

    '''
    A test case for function call.

    '''

    def wrap():

        print ('\n============= start testing %s function ======'
               '==========\n' % test_fun.__name__)

        test_fun()

        print ('\n============ end testing %s function ========'
               '==========\n' % test_fun.__name__)

    return wrap


def no_argument_decorator():

    '''
    function decorator with no argument.
    Usage example:
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


def no_argument_withwraps_decorator():

    '''
    function decorator with no argument.
    Usage example:
    >>> @no_argument_decorator()
    >>> def your_function(*args):
    >>>     write your own code
    At this time, you can't use as @no_argument_decorator,
    because your decorator function has no argument and
    decorator must callback with your_function as an argument.
    With the wraps decorator, you can see how and what the attributes of
    decorated function change.

    '''

    from functools import wraps

    def wrap(fun):

        show_name2address(fun)

        @wraps(fun)
        def innerwrap(*args):

            print 'execute in innerwrap'

            return fun(*args)

        show_name2address(innerwrap)

        return innerwrap

    show_name2address(wrap)

    return wrap


@test_case
def test_noarg_decorator_case():

    '''
    test no_argument_decorator with no argument for function

    '''
    try:

        @no_argument_decorator()
        def test_no_argument_decorator(*args):

            print 'execute in test_no_argument_decorator'

            print args

        print (test_no_argument_decorator.__dict__,
               test_no_argument_decorator.__name__)

    except Exception, e:

        print e

    # The address of test_no_argument_decorator function has been changed

    show_name2address(test_no_argument_decorator)

    # really, perform as invoking innerwrap functio

    test_no_argument_decorator(*[1, 'justdoit', 'programer'])


@test_case
def test_noarg_withwraps_decorator_case():

    '''
    test no_argument_decorator with no argument for function

    '''
    try:

        @no_argument_withwraps_decorator()
        def test_no_argument_withwraps_decorator(*args):

            print 'execute in test_no_argument_decorator'

            print args

        print (test_no_argument_withwraps_decorator.__dict__,
               test_no_argument_withwraps_decorator.__name__)

    except Exception, e:

        print e

    # The address of test_no_argument_decorator function has been changed

    show_name2address(test_no_argument_withwraps_decorator)

    # really, perform as invoking innerwrap functio

    test_no_argument_withwraps_decorator(*[1, 'justdoit', 'programer'])


@test_case
def test_noarg_decorator_class_case():

    '''
    test no_argument_decorator with no argument for class

    '''
    try:

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


@test_case
def test_noexplicitarg_decorator():

    '''
    Test no argument decorator with no explicit argument.

    '''

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
    Usage example:
    >>> @single_argument_decorator(default=below funtion)
    >>> def your_function(*args):
    >>>     write your own code
    '''

    show_name2address(fun)

    def wrap(*args):

        print args

        return fun(*args)

    return wrap


@test_case
def test_singlearg_decorator_case():

    try:

        @single_argument_decorator
        def test_single_argument_decorator(x):

            return x**2
    except Exception, e:

        print e

    print test_single_argument_decorator(3)


@test_case
def test_single_explicit_noarg_decorator_case():

    '''
    Test when single argument decorator is called with explicit no argument.

    '''

    try:

        @single_argument_decorator()
        def test_single_explicitno_argument_decorator(x):

            return 2*x
    except Exception, e:

        print e


def multi_arguments_decorator(fun, arg):

    '''
    function decorator with multi arguments.
    Usage example:
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


@test_case
def test_multiargs_decorator_case():

    '''
    Test function decorator with multi arguments.

    '''

    try:

        @multi_arguments_decorator(123, 'abc')
        def test_multi_arguments_decorator(s):

            print s

    except Exception, e:

        print e

    print test_multi_arguments_decorator('def')


@test_case
def test_noexplicitargs_decorator_case():

    '''
    Test function decorator without explicit arguments.

    '''

    try:

        @multi_arguments_decorator
        def test_multi_arguments_decorator(s):

            print s

    except Exception, e:

        print 'class decorator error!'

        print e


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


@test_case
def test_noarg_class_decorator_case():

    '''
    test function with no_argument_class_decorator.

    '''
    try:

        @no_argument_class_decorator
        def test_no_argument_class_decorator(s):

            return [x[:-2] for x in s]

    except Exception, e:

        print 'class decorator error'

        print e

    show_name2address(test_no_argument_class_decorator)

    test_no_argument_class_decorator(*('justdoit', 'basketball player'))

'''
def property_decorator(fun, *args):


    A property decorator for class object.
    Usage for example:
    >>> class A():
    >>> @property_decorator
    >>>     def class_fun(self):
    >>>         return 'class function'


    print 'execute in property decorator'

    print fun, dir(fun), fun.func_globals, args

    return fun(fun.im_self)
'''


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


@test_case
def test_property_decorator_case():

    '''
    Test self-implement property class

    '''

    tpd = test_property_decorator("mytest")

    print test_property_decorator.svalue, "tpd's value is %s" % tpd.svalue

    tpd._s = "new mytest"

    print "tpd's new value is %s" % tpd.svalue


'''
In python, we may use the multi levels decorators for different

decoration work.And the decorator order starts at definition of

function or class object from down to up.We can this in the

following example.Like this:

@decorator_b
@decorator_a
def myfunction():

  do_my_work

-----decoration order-----

@decorator_a
def myfunction():

  do_my_work

After this, a new function(eg: my_new_function) will be binded with

'my_function' name.

-----decorator order------

@decorator_b
my_new_function

And this becomes the usuall condition.

'''


def firstDecorator(fun):

    '''
    The first decorator when call with mutlti levels decorators.

    '''

    print 'execute in first decorator'

    def wrap(*args):

        fun(*args)

    return wrap


def secondDecorator(fun):

    '''
    The second decorator when call with mutlti levels decorators.

    '''

    print 'execute in second decorator'

    def wrap(*args):

        fun(*args)

    return wrap


@test_case
def test_multi_levels_decorator_case():

    @secondDecorator
    @firstDecorator
    def test_multi_levels_decorator(*args):

        '''
        Test how multi levels decorator works.

        '''

        print args

    test_multi_levels_decorator(*range(10))


def main():

    test_noarg_decorator_case()

    test_noarg_withwraps_decorator_case()

    test_noarg_decorator_class_case()

    test_noexplicitarg_decorator()

    test_singlearg_decorator_case()

    test_single_explicit_noarg_decorator_case()

    test_multiargs_decorator_case()

    test_noexplicitargs_decorator_case()

    test_noarg_class_decorator_case()

    test_property_decorator_case()

    test_multi_levels_decorator_case()


if __name__ == '__main__':

    main()
