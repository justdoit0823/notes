# -*- coding: utf-8 -*-


class DataProperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if not obj:
            return self
        return self.f(obj)

    def __set__(self, obj, value):
        raise AttributeError


class NondataProperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if not obj:
            return self
        return self.f(obj)


class testA(object):

    def __init__(self, x):
        self.x = x

    @DataProperty
    def dpx(self):
        return self.x


class testB(object):

    def __init__(self, y):
        self.y = y

    @NondataProperty
    def ndpy(self):
        return self.y


def main():

    a = testA(1234)
    print(a.dpx)  # read the dpx attribute of instance a
    # change the dpx key's value in dictionary of a
    a.__dict__['dpx'] = 'new dpx'
    print(a.dpx)
    b = testB(4567)
    print(b.ndpy)
    b.__dict__['ndpy'] = 'new ndpy'
    print(b.ndpy)


if __name__ == '__main__':

    main()
