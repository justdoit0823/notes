
"""Show duplicated fd information."""

import os
import socket


def show_fd_info(fd):
    """Show fd information."""
    pid = os.getpid()
    os.system('stat /proc/{0}/fd/{1}'.format(pid, fd))


def dup_socket():
    s_sock = socket.socket()
    s_sock.bind(('127.0.0.1', 0))
    s_sock.listen(5)

    show_fd_info(s_sock.fileno())

    new_fd = os.dup(s_sock.fileno())
    show_fd_info(new_fd)

    return s_sock


def dup_file():
    fd = os.open('/proc/cpuinfo', os.O_RDONLY)
    show_fd_info(fd)

    new_fd = os.dup(fd)
    show_fd_info(new_fd)

    return fd


def main():
    s_sock = dup_socket()
    fd = dup_file()

    pid = os.fork()
    if pid == -1:
        raise RuntimeError

    if pid == 0:
        show_fd_info(fd)
        show_fd_info(s_sock.fileno())
    else:
        os.waitpid(pid, 0)

    os.close(fd)


if __name__ == '__main__':
    main()
