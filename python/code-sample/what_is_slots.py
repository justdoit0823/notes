# -*- coding: utf-8 -*-

'''
This is a example for python slots usage.
See more detail at https://docs.python.org/2/reference/datamodel.html#slots.
'''


class ASlots(object):
    __slots__ = 'x', 'y'


class BNoSlots(object):
    pass


class CSlots:
    __slots__ = 'x', 'y'


class D:
    pass


class ESlots(D):
    __slots__ = 'x', 'y'


class FSlotsWithDict(object):
    __slots__ = 'x', 'y', '__dict__'


def main():
    print(ASlots.__dict__)
    print(ASlots.x, ASlots.y)
    print(type(ASlots.x), type(ASlots.y))
    a1 = ASlots()
    a1.x = 10
    a1.y = 'python'
    print(a1.x, a1.y)
    try:
        a1.z = (1,)
    except AttributeError:
        print('set attribute z with instance a1 failure')
    try:
        print(a1.__dict__)
    except AttributeError:
        print('no __dict__ attribute in instance a1')
    print(BNoSlots.__dict__)
    b1 = BNoSlots()
    try:
        b1.z = (1,)
    except AttributeError:
        print('set attribute z with instance b1 failure')
    print(b1.z)
    print(b1.__dict__)
    print(CSlots.__dict__)
    try:
        print(CSlots.x, CSlots.y)
    except AttributeError:
        print('no this attribute')
    c1 = CSlots()
    c1.x = 100
    c1.y = 'python3'
    print(c1.x, c1.y)
    try:
        c1.z = (1, 2)
    except AttributeError:
        print('set attribute z with instance c failure')
    print(c1.z)
    print(c1.__dict__)
    print(ESlots.__dict__)
    try:
        print(ESlots.x, ESlots.y)
    except AttributeError:
        print('no this attribute')
    e1 = ESlots()
    e1.x = 1000
    e1.y = 'python3.4'
    print(e1.x, e1.y)
    try:
        e1.z = (1, 2, 3)
    except AttributeError:
        print('set attribute z with instance e1 failure')
    print(e1.__dict__)
    print(FSlotsWithDict.__dict__, type(FSlotsWithDict.__dict__))
    print(FSlotsWithDict.x, FSlotsWithDict.y,
          FSlotsWithDict.__dict__['__dict__'])
    print(type(FSlotsWithDict.x), type(FSlotsWithDict.y),
          type(FSlotsWithDict.__dict__['__dict__']))
    f1 = FSlotsWithDict()
    f1.x = 10000
    f1.y = 'python-3.4'
    print(f1.x, f1.y)
    try:
        f1.z = (1, 2, 3, 4)
    except AttributeError:
        print('set attribute z with instance f1 failure')
    print(f1.z)
    print(f1.__dict__)


if __name__ == '__main__':
    main()
