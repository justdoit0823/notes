# -*- coding: utf-8 -*-

'''
The class and object access attribute order is followed:

First, look at class attribute access order.

1. Look into meta class's mro class list dictionary for the specified
attribute, if found and this is a data descriptor, then use it.

2. The founded attribute is a non-data descriptor or not a descriptor,
look into class's mro class list dictionary.If found and this is a descriptor,
then use it with descriptor protocol.Or just use it.

3. Not found in class's mro class list dictionary, if the attribute found in
meta class's mro class list dictionary and is a non-data descriptor,
then use it with descriptor protocol.Or just use it as usual.

4. Raise attribute exception.

Second, look at object attribute access order.

1. Look into object's class mro dictionary list for the specified attribute,
if found and this is a data descriptor, then use it.

2. The founded attribute is a non-dta descriptor or not a descriptor,
look into object's dictionary.If found, then use it.

3. Not found in object's dictionary, if the attribute found in object's class
mro dictionary list and whether is a non-data descriptor, then use it.

4. Raise attribute exception.
'''


class A(object):

    def __getattribute__(self, name):
        print('in class A getattribute method')
        return object.__getattribute__(self, name)


class B(A):

    def __getattribute__(self, name):
        print('in class B getattribute method')
        return A.__getattribute__(self, name)


class C(B):

    def __getattr__(self, name):
        print('in class C getattr method')
        return B.__getattr__(self, name)


class D(C):

    def __getattribute__(self, name):
        print('in class D getattribute method')
        if name == 'xy' and name not in self.__dict__:
            self.__dict__[name] = 12345
        return C.__getattribute__(self, name)

    def __getattr__(self, name):
        print('in class D getattr method')
        return C.__getattr__(self, name)


class E(D):

    xyz = 1234567

    def __getattr__(self, name):
        print('in class E getattr method')
        return D.__getattr__(self, name)


class F(E):

    @classmethod
    def cmfun(cls):
        print('in class F cmfun method')


class MyClassmethod(classmethod):

    def __get__(self, obj, cls=None):
        print('in MyClassmethod get method')
        return classmethod.__get__(self, obj, cls)


class G(F):

    @MyClassmethod
    def cmfun(cls):
        print('in class G cmfun method')


def main():

    a = A()
    b = B()
    c = C()
    d = D()
    e = E()
    f = F()
    g = G()
    try:
        a.xy
    except:
        print('attribute error')
    try:
        b.xy
    except:
        print('attribute error')
    try:
        c.xy
    except:
        print('attribute error')
    try:
        d.xy = 123456
        print(d.xy)
    except:
        print('attribute error')
    try:
        # e.xyz = 12345678
        print(e.xyz)
    except:
        print('attribute error')
    try:
        f.cmfun()
    except:
        print('attribute error')
    try:
        print(g.__dict__)
        g.cmfun()
    except:
        print('attribute error')


if __name__ == '__main__':

    main()
