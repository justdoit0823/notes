# -*- coding: utf-8 -*-


import sys


class A(object):

    def foo(self):
        print('in method foo')
    print(foo, hex(id(foo)))


class Z(object):

    @classmethod
    def foo():
        print('in method foo')
    print(foo, hex(id(foo)))


def main():

    print(A.__dict__['foo'], hex(id(A.__dict__['foo'])))
    print(A.foo, hex(id(A.foo)), A.foo.im_self, A.foo.im_func, A.foo.im_class)
    a = A()
    print(a.foo, hex(id(a.foo)), a.foo.im_self, a.foo.im_func, a.foo.im_class)
    print('unbound method equal to bound method', A.foo is a.foo)
    # print(sys.getsizeof(A.foo), sys.getsizeof(a.foo))
    print(A.foo.__dict__, a.foo.__dict__)
    print(type(A.foo), type(a.foo))
    # print(A.foo.__mro__, a.foo.__mro__)
    print('========================================')
    print(Z.__dict__['foo'], hex(id(Z.__dict__['foo'])))
    print(Z.foo, hex(id(Z.foo)), Z.foo.im_self, Z.foo.im_func, Z.foo.im_class)
    z = Z()
    print(z.foo, hex(id(z.foo)), z.foo.im_self, z.foo.im_func, z.foo.im_class)
    print('unbound method equal to bound method', Z.foo is z.foo)
    # print(sys.getsizeof(Z.foo), sys.getsizeof(z.foo))
    print(Z.foo.__dict__, z.foo.__dict__)
    print(type(Z.foo), type(z.foo))


if __name__ == '__main__':

    main()
