
"""Show socket's keepalive semantics.

Read more details at https://tools.ietf.org/html/rfc1122#page-101,
section 4.2.3.6  TCP Keep-Alives.

"""

import click
import os
import socket
import threading
import time


default_host = '127.0.0.1'
default_port = 11111


@click.group()
def main():
    """Execution entry."""
    pass


@main.command(name='run_server')
@click.argument('host', default=default_host)
@click.argument('port', default=default_port)
def server(**kwargs):
    """Start test server."""
    host = kwargs['host']
    port = int(kwargs['port'])

    server_socket = socket.socket()

    server_socket.bind((host, port))
    server_socket.listen(5)

    print('run server on {0}:{1}...'.format(host, port))

    while True:
        sock_obj, sock_addr = server_socket.accept()
        print('receive conenction from {0}:{1}'.format(*sock_addr))


@main.command(name='run_client')
@click.argument('host', default=default_host)
@click.argument('port', default=default_port)
@click.argument('keepidle', default=120)
@click.argument('keepcnt', default=5)
@click.argument('keepinterval', default=30)
def client(**kwargs):
    """Start test client."""
    host = kwargs['host']
    port = int(kwargs['port'])
    keepidle = int(kwargs['keepidle'])
    keepcnt = int(kwargs['keepcnt'])
    keepinterval = int(kwargs['keepinterval'])

    client_socket = socket.socket()
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    client_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, keepcnt)
    client_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, keepinterval)
    client_socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, keepidle)

    client_socket.connect((host, port))
    print('connect to server at {0}:{1} with local socket {2}:{3}'.format(
        host, port, *client_socket.getsockname()))

    exit_event = threading.Event()
    endpoint = ':'.join(map(str, client_socket.getsockname()))

    def print_keepalive_info(endpoint, exit_event):
        while not exit_event.is_set():
            os.system("ss -tnpo|awk '$4 == \"{0}\"'".format(endpoint))
            time.sleep(3)

    print_thread = threading.Thread(
        target=print_keepalive_info, args=(endpoint, exit_event))
    print_thread.start()

    client_socket.send(b'hello')
    try:
        while True:
            if not client_socket.recv(1024):
                break
    finally:
        exit_event.set()


if __name__ == '__main__':

    main()
