
"""Comapre epoll level trigger and edge trigger."""

import os
import select
import socket
import sys
import time


def bind_local_server(port):
    s_sock = socket.socket()
    s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s_sock.bind(('127.0.0.1', port))
    s_sock.listen(128)

    return s_sock


def pick_connection(sock, pick_timeout):
    picked_cnt = 0
    sock.setblocking(False)
    while True:
        try:
            __, __ = sock.accept()
        except OSError as e:
            if e.errno == socket.EAGAIN:
                break
        else:
            picked_cnt += 1

        time.sleep(pick_timeout)

    print('socket', sock.fileno(), 'picked', picked_cnt, 'conenctions')


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
    cmd = 'ss -tnlp|grep 127.0.0.1:{0}'.format(port)
    os.system(cmd)


def pick_conenctions(sock, num):
    sock.setblocking(False)

    pick_cnt = 0
    socks = []
    while num > 0:
        try:
            ac_sock, __ = sock.accept()
        except OSError as e:
            if e.errno == socket.EAGAIN:
                break
        else:
            socks.append(ac_sock)
            num -= 1
            pick_cnt += 1

    print('picked', pick_cnt, 'connections')
    return socks


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
    flags = select.EPOLLIN
    if edge_mode:
        flags |= select.EPOLLET

    poll_obj.register(server_fd, flags)

    client_socks = make_connection(port, 10)
    ac_socks = []

    ret = poll_obj.poll(timeout=2)
    if ret and ret[0][0] == server_fd and ret[0][1] & select.EPOLLIN:
        ac_socks.extend(pick_conenctions(server_sock_1, num=5))

    show_stat_info(port)

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)
    if ret and ret[0][0] == server_fd and ret[0][1] & select.EPOLLIN:
        ac_socks.extend(pick_conenctions(server_sock_1, num=3))

    client_socks.extend(make_connection(port, num=2))
    show_stat_info(port)

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)
    if ret and ret[0][0] == server_fd and ret[0][1] & select.EPOLLIN:
        ac_socks.extend(pick_conenctions(server_sock_1, num=3))

    c_map = {c_sock.getsockname(): c_sock for c_sock in client_socks}

    c_flags = select.EPOLLIN
    if edge_mode:
        c_flags |= select.EPOLLET

    client_fd = ac_socks[0].fileno()
    poll_obj.register(client_fd, c_flags)
    peername = ac_socks[0].getpeername()
    c_map[peername].send(b'Hello, this is from {0}'.format(peername))

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)
    for pair in ret:
        if pair[0] == client_fd and pair[1] & select.EPOLLIN:
            ac_socks[0].recv(10)

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)
    for pair in ret:
        if pair[0] == client_fd and pair[1] & select.EPOLLIN:
            ac_socks[0].recv(20)

    c_map[peername].send(b'Hello, this is from {0}'.format(peername))

    show_stat_info(port)

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)

    c_map[peername].send(b'Hello, this is from {0}'.format(peername))

    show_stat_info(port)

    poll_s_time = time.time()
    ret = poll_obj.poll(timeout=3)
    poll_e_time = time.time()
    print('poll wait time', poll_e_time - poll_s_time)
    for pair in ret:
        if pair[0] == client_fd and pair[1] & select.EPOLLIN:
            ac_socks[0].recv(1024)

    server_sock_1.close()
    print('stop test server.')


if __name__ == '__main__':

    main()
