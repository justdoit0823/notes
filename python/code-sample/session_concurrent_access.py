
import threading

import click

from utils.sql import autocommit_scope


@autocommit_scope(using='local')
def sleep_query(session):
    ret = session.execute('select sleep(10);')
    print(ret)


@autocommit_scope(using='local')
def simple_query(session):
    ret = session.execute('select 1;').first()
    print(ret)


@click.group()
def main():
    pass


@main.command('run', help='concurrent session access.')
def run():

    thread1 = threading.Thread(target=sleep_query)
    thread2 = threading.Thread(target=simple_query)

    print('start test...')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    print('finish...')


if __name__ == '__main__':
    main()
