
"""Check how epoll works."""

import click
import errno
import os
import select
import socket
import threading
import time


__all__ = ['run_client', 'run_server']


@click.group()
def main():
    pass


@main.command('run_server')
@click.argument('host')
@click.argument('port')
@click.argument('et_mode', default=0)
def run_server(**kwargs):
    """Run test epoll server."""
    host = kwargs['host']
    port = kwargs['port']
    et_mode = bool(int(kwargs['et_mode']))

    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_sock.setblocking(0)
    s_sock.bind((host, int(port)))
    s_sock.listen(5)

    def loop():
        ep = select.epoll()
        ep_flag = select.EPOLLIN
        if et_mode:
            ep_flag |= select.EPOLLET

        ep.register(s_sock.fileno(), ep_flag)
        while True:
            try:
                ep_ret = ep.poll()
            except OSError as e:
                if e.errno == errno.EINTR:
                    break
            else:
                print(os.getpid(), ep_ret)
                while True:
                    try:
                        s_sock.accept()
                    except OSError as e:
                        if e.errno == errno.EAGAIN:
                            print(
                                'failure in process', os.getpid(),
                                errno.errorcode[e.errno])
                            break
                    else:
                        print('accept success', os.getpid())


    pid = os.fork()
    if pid == -1:
        exit(0)

    if pid == 0:
        loop()
        time.sleep(3)
    else:
        loop()
        os.waitpid(pid)


@main.command('run_thread_server')
@click.argument('host')
@click.argument('port')
@click.argument('et_mode', default=0)
@click.argument('thread_num', default=2)
def run_thread_server(**kwargs):
    """Run test epoll server in threaad mode."""
    host = kwargs['host']
    port = kwargs['port']
    et_mode = bool(int(kwargs['et_mode']))
    thread_num = int(kwargs['thread_num'])

    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_sock.setblocking(0)
    s_sock.bind((host, int(port)))
    s_sock.listen(5)

    ep = select.epoll()
    ep_flag = select.EPOLLIN
    if et_mode:
        ep_flag |= select.EPOLLET

    ep.register(s_sock.fileno(), ep_flag)

    def loop():
        while True:
            try:
                ep_ret = ep.poll()
            except OSError as e:
                if e.errno == errno.EINTR:
                    break
            else:
                print(threading.get_ident(), ep_ret)
                while True:
                    try:
                        s_sock.accept()
                    except OSError as e:
                        if e.errno == errno.EAGAIN:
                            print(
                                'failure in process', threading.get_ident(),
                                errno.errorcode[e.errno])
                            break
                    else:
                        print('accept success', threading.get_ident())

    thread_list = []
    for i in range(thread_num):
        thread_obj = threading.Thread(target=loop)
        thread_list.append(thread_obj)

    for thread in thread_list:
        thread.start()
        print('thread ', thread.ident, 'start...')

    for thread in thread_list:
        thread.join()


@main.command('run_client')
@click.argument('host')
@click.argument('port')
def run_client(**kwargs):
    """Run test client."""
    host = kwargs['host']
    port = kwargs['port']

    c_sock = socket.socket()
    c_sock.connect((host, int(port)))
    print('connect success...')

    time.sleep(2)

    c_sock.close()


if __name__ == '__main__':

    main()
