
"""Inspect PostgreSQL command id."""

import sys

import psycopg2


def query_result(cursor, rel_name):
    """Execute sql query."""
    cursor.execute('select xmin, xmax, cmin, cmax, * from {0}'.format(rel_name))
    return cursor.fetchall()

def show_result(label, res):
    print('========== begin {0} query====='.format(label))

    print('xmin, xmax, cmin, cmax, *')
    for row in res:
        print(' '.join(map(str, row)))

    print('========== end {0} query====='.format(label))


def get_new_connection(host, port, user, password):
    """Initialize a new connection."""
    return psycopg2.connect(
        host=host, port=port, user=user, password=password, dbname='postgres')


def create_test_relation(cursor, rel_name):
    cursor.execute('create table if not exists {0}(id int)'.format(rel_name))


def main():
    if len(sys.argv) < 5:
        print('python postgresql_command_id.py host port user password')
        return 0

    host = sys.argv[1]
    port = int(sys.argv[2])
    user = sys.argv[3]
    password = sys.argv[4]

    rel_name = 's_test_command_id'

    con = get_new_connection(host, port, user, password)

    with con.cursor() as cursor:
        create_test_relation(cursor, rel_name)

    cursor = con.cursor()
    cursor.execute('insert into {0} values(1)'.format(rel_name))
    show_result('first cursor', query_result(cursor, rel_name))

    mid_cursor = con.cursor()
    mid_cursor.execute('select xmin, xmax, cmin, cmax, * from {0}'.format(rel_name))
    show_result('first cursor', query_result(cursor, rel_name))

    new_cursor = con.cursor()
    new_cursor.execute('insert into {0} values(2)'.format(rel_name))
    show_result('new cursor', query_result(new_cursor, rel_name))

    show_result('mid cursor', mid_cursor.fetchall())


if __name__ == '__main__':
    main()
