
"""PostgreSQL advisory lock."""

import multiprocessing
import sys
import time

import psycopg2


def get_connection(dsn):
    return psycopg2.connect(dsn=dsn)


def _pg_advisory_lock(connection, key):
    cursor = connection.cursor()
    cursor.execute('select pg_advisory_lock(%s)', (key,))
    cursor.close()


def _pg_advisory_unlock(connection, key):
    cursor = connection.cursor()
    cursor.execute('select pg_advisory_unlock(%s)', (key,))
    ret = cursor.fetchone()[0]
    cursor.close()
    return ret


class Lock:

    def __init__(self, connection):
        self._conn = connection

    def acquire(self, key):
        _pg_advisory_lock(self._conn, key)

    def release(self, key):
        _pg_advisory_lock(self._conn, key)


def test_lock(dsn, key):
    connection = get_connection(dsn)
    connection.set_session(autocommit=True)
    lock = Lock(connection)

    lock.acquire(key)
    print('acquire the lock', key, multiprocessing.current_process())

    time.sleep(3)
    print('after sleep 3 seconds...', multiprocessing.current_process())

    lock.release(key)

    connection.close()


def main():
    dsn = 'user=postgres port=5442' if len(sys.argv) == 1 else sys.argv[1]
    key = 1234567890

    processes = [
        multiprocessing.Process(target=test_lock, args=(dsn, key))
        for idx in range(8)]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
