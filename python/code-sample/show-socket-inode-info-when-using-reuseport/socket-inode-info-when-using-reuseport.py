
"""reuse port socket test module."""

import os
import socket
import sys


def bind_local_server(port):
    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s_sock.bind(('127.0.0.1', port))
    s_sock.listen(5)

    return s_sock


def show_sock_info(sock, inherited_fd=0, sock_prefix=''):
    pid = os.getpid()
    fd = sock.fileno()
    sock_stat = os.stat('/proc/{0}/fd/{1}'.format(pid, fd))
    print('server {0} socket fd {1}, inode {2}.'.format(
        sock_prefix, fd, sock_stat.st_ino))

    if inherited_fd:
        inherited_sock_stat = os.stat(
            '/proc/{0}/fd/{1}'.format(pid, inherited_fd))
        print('inherited {0} socket fd {1}, inode {2}'.format(
            sock_prefix, inherited_fd, inherited_sock_stat.st_ino))


def bind_first_server(port):
    s_sock = bind_local_server(port)
    dup_fd = os.dup(s_sock.fileno())
    show_sock_info(s_sock, inherited_fd=dup_fd, sock_prefix='#1')
    return s_sock


def bind_second_server(port, inherited_fd):
    s_sock = bind_local_server(port)
    show_sock_info(s_sock, inherited_fd=inherited_fd, sock_prefix='#2')
    return s_sock


def main():
    if len(sys.argv) < 2:
        print('local server port is needed.')
        return

    port = int(sys.argv[1])

    server_sock = bind_first_server(port)
    fd = server_sock.fileno()

    pid = os.fork()
    if pid == -1:
        print('fork error.')
        return

    if pid == 0:
        server_sock = bind_second_server(port, fd)
        server_sock.close()
        print('stop second server.')
        exit(0)

    os.waitpid(pid, 0)

    server_sock.close()
    print('stop first server.')


if __name__ == '__main__':

    main()
