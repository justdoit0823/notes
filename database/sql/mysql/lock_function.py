
"""Use lock function in mysql."""

import argparse
import time

from MySQLdb import connect


def get_connection(host='localhost', port=3306, user=None, passwd=''):
    """Return mysql connection."""
    return connect(host=host, port=port, user=user, passwd=passwd)


def _mysql_acquire_lock(connection, identity, timeout):
    """Acquire MySQL lock."""
    cursor = connection.cursor()
    cursor.execute("select get_lock(%s, %s)", (identity, timeout))
    acquired = cursor.fetchone()[0]

    if acquired == 1:
        return 1
    elif acquired == 0:
        raise TimeoutError('timeout exceeds.')

    raise Exception('error')


def _mysql_release_lock(connection, identity):
    """Release MySQL lock."""
    cursor = connection.cursor()
    cursor.execute("select release_lock(%s)", (identity,))
    released = cursor.fetchone()[0]

    if released == 1:
        return 1
    elif released == 0:
        raise ValueError('Current connection does not hold the lock.')

    raise ValueError('invalid lock identity.')


class Lock:

    def __init__(self, connection, timeout=None):
        self._conn = connection
        self._timeout = timeout

    def acquire(self, identity, timeout=None):
        timeout = timeout or self._timeout
        if timeout is None:
            timeout = -1

        return _mysql_acquire_lock(self._conn, identity, timeout)

    def release(self, identity):
        return _mysql_release_lock(self._conn, identity)


def main():
    """Test main entry."""
    parser = argparse.ArgumentParser(description='Test mysql lock function.')
    parser.add_argument(
        '--user', dest='user', action='store', default='root',
        help='mysql user.')
    args = parser.parse_args()

    connection = get_connection(user=args.user)

    identity = 'test_lock_123456789'
    lock = Lock(connection, 10)

    try:
        lock.acquire(identity, None)
    except TimeoutError:
        print('acquire timeout.')
    except Exception as e:
        print(e)
        print('acquire failed.')
    else:
        print('acquire success.')
        time.sleep(15)

        lock.release(identity)


if __name__ == '__main__':
    main()
