
# -*- coding: utf-8 -*-

"""探测监听套接字backlog对应的长度。"""

import click
import socket
import time


default_host = '127.0.0.1'
default_port = 11111
default_backlog = 128


@click.group()
def main():

    pass

@main.command(name='run_server')
@click.argument('host', default=default_host)
@click.argument('port', default=default_port)
@click.argument('backlog', default=default_backlog)
def server(**kwargs):

    host = kwargs['host']
    port = int(kwargs['port'])
    backlog = int(kwargs['backlog'])

    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen(backlog)

    print('run server on {0}:{1} with backlog {2}...'.format(
        host, port, backlog))

    while True:
        time.sleep(1)


@main.command(name='run_client')
@click.argument('host', default=default_host)
@click.argument('port', default=default_port)
@click.argument('detect_num', default=default_backlog)
def client(**kwargs):

    host = kwargs['host']
    port = int(kwargs['port'])
    detect_num = int(kwargs['detect_num'])

    count = 0
    detected_num = 0

    while detected_num < detect_num:
        client_socket = socket.socket()
        try:
            client_socket.connect((host, port))
            # except ConnectionRefusedError:
        except OSError as e:
            print(e)
            break
        else:
            count += 1
            # time.sleep(1)

        detected_num += 1

    print('detect {0} times and success {1}.'.format(detected_num, count))


if __name__ == '__main__':

    main()
