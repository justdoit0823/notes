
"""Show what happens after poping imported module."""

import sys


def main():
    import example_module
    print(example_module.foo, id(example_module.foo))

    del example_module

    import example_module
    print(example_module.foo, id(example_module.foo))

    del example_module
    del sys.modules['example_module']

    import example_module
    print(example_module.foo, id(example_module.foo))


if __name__ == '__main__':
    main()
