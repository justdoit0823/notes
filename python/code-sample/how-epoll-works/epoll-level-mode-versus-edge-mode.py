
"""Comapre epoll level trigger and edge trigger."""

import errno
import functools
import os
import select
import socket
import sys
import time


fd_handlers = {}
fd_socks = {}
ac_socks = []


def bind_local_server(port):
    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s_sock.bind(('127.0.0.1', port))
    s_sock.listen(128)

    return s_sock


def make_connection(port, num=100):
    con_cnt = 0
    socks = []
    while num > 0:
        c_sock = socket.socket()
        c_sock.connect(('127.0.0.1', port))
        socks.append(c_sock)
        num -= 1
        con_cnt += 1

    print('already made %d conenctions.' % con_cnt)

    return socks


def show_stat_info(port):
    cmd = "ss -tnap|grep 127.0.0.1:{0}|awk '$2 > 0'".format(port)
    os.system(cmd)


def pick_conenctions(sock, num):
    sock.setblocking(False)

    pick_cnt = 0
    socks = []
    while num > 0:
        try:
            ac_sock, __ = sock.accept()
        except socket.error as e:
            if e.errno == errno.EAGAIN:
                break
        else:
            socks.append(ac_sock)
            num -= 1
            pick_cnt += 1

    print('picked %d connections.' % pick_cnt)
    return socks


def poll(poll_obj, timeout=-1):
    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=timeout)
    poll_e_time = time.time()
    duration = poll_e_time - poll_s_time

    print('poll wait time %f, and ret %s.' % (duration, ret))

    for fd, event in ret:
        try:
            handler = fd_handlers[fd]
        except KeyError:
            continue
        else:
            handler(fd, event)

    return duration


def handle_server_event(ac_num, fd, event):
    print('\n')
    server_sock = fd_socks[fd]
    if event & select.EPOLLIN:
        ac_socks.extend(pick_conenctions(server_sock, num=ac_num))


def handle_client_event(b_cnt, fd, event):
    c_sock = fd_socks[fd]
    if event & select.EPOLLIN:
        data = c_sock.recv(b_cnt)
        print('\nreceived %d bytes.\n' % len(data))


def send_data(sock, data):
    sock.send(data.encode())
    print('fd %d sent %d bytes.' % (sock.fileno(), len(data)))


def main():
    if len(sys.argv) < 2:
        print('local server port is needed.')
        return

    port = int(sys.argv[1])
    edge_mode = 0
    if len(sys.argv) >= 3:
        edge_mode = int(sys.argv[2])

    poll_obj = select.epoll()

    server_sock_1 = bind_local_server(port)
    server_fd = server_sock_1.fileno()
    fd_socks[server_fd] = server_sock_1
    flags = select.EPOLLIN
    if edge_mode:
        flags |= select.EPOLLET

    poll_obj.register(server_fd, flags)

    client_socks = make_connection(port, 10)
    show_stat_info(port)

    fd_handlers[server_fd] = functools.partial(handle_server_event, 5)
    duration = poll(poll_obj, timeout=3)
    assert duration < 1, "poll duration is too long"

    show_stat_info(port)

    fd_handlers[server_fd] = functools.partial(handle_server_event, 3)
    duration = poll(poll_obj, timeout=3)
    if duration >= 3:
        print('[EDGE TRIGGERED] left ready connections were not reported.\n')

    print('\n')

    client_socks.extend(make_connection(port, num=2))
    show_stat_info(port)

    duration = poll(poll_obj, timeout=3)
    if duration > 1:
        print('[WARNING] new ready connections were not reported.\n')
    else:
        print('[OK] new incoming packet event is expected.\n')

    c_map = {c_sock.getsockname(): c_sock for c_sock in client_socks}
    c_flags = select.EPOLLIN
    if edge_mode:
        c_flags |= select.EPOLLET

    c_sock = ac_socks[0]
    client_fd = c_sock.fileno()
    poll_obj.register(client_fd, c_flags)
    fd_socks[client_fd] = c_sock

    peername = c_sock.getpeername()
    client_peer = c_map[peername]
    print('\n')
    send_data(client_peer, 'Hello, this is from {0}'.format(peername))
    show_stat_info(port)
    print('\n')

    fd_handlers[client_fd] = functools.partial(handle_client_event, 10)
    duration = poll(poll_obj, timeout=3)
    if duration > 1:
        print('[WARNING] new incoming packet was not reported.\n')

    show_stat_info(port)

    fd_handlers[client_fd] = functools.partial(handle_client_event, 20)
    duration = poll(poll_obj, timeout=3)
    if duration >= 3:
        print('[EDGE TRIGGERED] left partial packet was not reported.\n')

    send_data(client_peer, 'Hello, this is from {0}'.format(peername))
    show_stat_info(port)
    print('\n')

    fd_handlers[client_fd] = functools.partial(handle_client_event, 50)
    duration = poll(poll_obj, timeout=3)
    if duration > 1:
        print('[WARNING] new incoming packet was not reported.\n')
    else:
        print('[OK] new incoming packet event is expected.\n')

    server_sock_1.close()
    print('stop test server.')


if __name__ == '__main__':

    main()
