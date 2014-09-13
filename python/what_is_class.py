# -*- coding: utf-8 -*-

'''
This module shows how different class methods work and mean.

'''


class A():

    def foo(self, f):
        '''
        This is a normal method of class.

        '''

        print self, f


class B():

    @classmethod
    def foo(cls, f):
        '''
        This is a class method.

        '''

        print cls, f

#        print 'class method'


class C():

    @staticmethod
    def foo(f):
        '''
        This is a static method in class.

        '''

        print f


'''
How super works in python multiple class inheritance.
The form of super(Subclass, self).method() will call
both BaseClass method in order.And super(Baseclass, self).method()
will call the Baseclass's common base class method at last,
while only call first Baseclass's base class method.
'''


class BaseClass(object):

    def f(self):
        print 'method f in BaseClass'


class NotBaseClass(object):

    def f(self):

        print 'method f in NotBaseClass'


class LeftClass(BaseClass):

    def f(self):
        print 'method f in LeftClass'
        super(LeftClass, self).f()


class RightClass(BaseClass):

    def f(self):

        print 'method f in RightClass'
        super(RightClass, self).f()


class MergeClass(LeftClass, RightClass):

    def f(self):

        print 'method f in MergeClass'
        super(MergeClass, self).f()


def main():

    print A, A.foo, hex(id(A)), hex(id(A.foo)), hex(id(A.foo.__func__))

    print B, B.foo, hex(id(B)), hex(id(B.foo)), hex(id(B.foo.__func__))

    print type(A.foo), type(B.foo), A.foo == B.foo

    print C, C.foo, hex(id(C)), hex(id(C.foo))

    a = A()

    b = B()

    c = C()

    print a, a.foo, hex(id(a)), hex(id(a.foo)), hex(id(a.foo.__func__))

    print b, b.foo, hex(id(b)), hex(id(b.foo)), hex(id(b.foo.__func__))

    print c, c.foo, hex(id(c)), hex(id(c.foo))

    try:
        A.foo('call class method')
    except Exception, e:
        print e

    A.foo(a, 'call class method with instance')

    a.foo('call instance method')

    B.foo('call class method')

    b.foo('call instance method')

    C.foo('call class method')

    c.foo('call instance method')

    # print class mro

    print BaseClass.__mro__

    print NotBaseClass.__mro__

    print LeftClass.__mro__

    print RightClass.__mro__

    print MergeClass.__mro__

    merge = MergeClass()

    merge.f()

    print merge, dir(merge), merge.__subclasshook__, \
        dir(merge.__subclasshook__)


if __name__ == '__main__':

    main()
