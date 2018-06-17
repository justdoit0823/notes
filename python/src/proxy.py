
"""Python proxy implementation example."""


class Hello:

    def __init__(self, name):
        self._name = name

    def greeting(self, to):
        print('Hi', to, 'from', self._name)

    def show(self):
        print("This is", self._name)


class HelloProxy:

    __slots__ = ('_inst',)

    def __init__(self, instance):
        # Note: attribute `_inst` is a slot descriptor
        self._inst = instance

    def __getattribute__(self, name):
        try:
            # Match proxy object attributes first
            return super(HelloProxy, self).__getattribute__(name)
        except AttributeError:
            return self._inst.__getattribute__(name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            # Need for proxy object initialization
            return super(HelloProxy, self).__setattr__(name, value)

        return self._inst.__setattr__(name, value)


def main():
    h1 = Hello('Python')
    p1 = HelloProxy(h1)

    h1.greeting('Java')
    p1.greeting('Java')

    h1.show()
    p1.show()

    p1.rate = 1000
    print(h1.rate)
    print(p1.rate)


if __name__ == '__main__':
    main()
