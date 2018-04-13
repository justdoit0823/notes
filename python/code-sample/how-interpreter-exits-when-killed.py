
import os
import time


class A:

    def __del__(self):
        print('del', flush=True)


def main():
    print('process', os.getpid(), flush=True)
    a = A()
    print(a)

    try:
        time.sleep(30)
    except Exception as e:
        print('exception', e, flush=True)
    finally:
        print('finally', flush=True)


if __name__ == '__main__':
    main()
