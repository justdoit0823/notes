
"""Compare packet transfer by tcp versus udp."""

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


def bind_local_tcp_server(port):
    s_sock = socket.socket()
    s_sock.bind(('127.0.0.1', port))
    s_sock.listen(128)

    return s_sock


def bind_local_udp_server(port):
    s_sock = socket.socket(type=socket.SOCK_DGRAM)
    s_sock.bind(('127.0.0.1', port))

    return s_sock


def show_stat_info(port, tcp=True, gt_zero=True):
    if tcp:
        cmd = "ss -tnap"
    else:
        cmd = "ss -unap"

    cmd = cmd + "|awk '$4 == \"127.0.0.1:{0}\"'".format(port)

    if gt_zero:
        cmd = cmd + "|awk '$2 > 0'"

    os.system(cmd)


def main():
    if len(sys.argv) < 2:
        print('local server port is needed.')
        return

    port = int(sys.argv[1])

    tcp_server_sock = bind_local_tcp_server(port)
    udp_server_sock = bind_local_udp_server(port)

    show_stat_info(port)

    tcp_client_sock = socket.socket()
    tcp_client_sock.connect(('127.0.0.1', port))

    show_stat_info(port)

    tcp_ac_sock, __ = tcp_server_sock.accept()
    show_stat_info(port)

    s_data = 'Hello world.'
    tcp_client_sock.send(s_data.encode())
    print('sent data "%s" by tcp endpoint.' % s_data)
    show_stat_info(port)

    r_data = tcp_ac_sock.recv(10)
    print('\nreceived data "%s", %d bytes from tcp endpoint.' % (r_data, len(r_data)))
    show_stat_info(port)

    r_data = tcp_ac_sock.recv(10)
    print('received data "%s", %d bytes from tcp endpoint.' % (r_data, len(r_data)))
    show_stat_info(port, gt_zero=False)

    s_data_1 = 'Beautiful is better than ugly.'
    s_data_2 = 'Explicit is better than implicit.'
    tcp_client_sock.send(s_data_1.encode())
    tcp_client_sock.send(s_data_2.encode())
    print('\nsent data "%s%s" by tcp endpoint.' % (s_data_1, s_data_2))
    show_stat_info(port)

    r_data = tcp_ac_sock.recv(1024)
    print('received data "%s", %d bytes from tcp endpoint.\n' % (r_data, len(r_data)))
    show_stat_info(port)

    udp_client_sock = socket.socket(type=socket.SOCK_DGRAM)

    s_data = 'Hello world.'
    udp_client_sock.sendto(s_data.encode(), ('127.0.0.1', port))
    print('sent data "%s" by udp endpoint.' % s_data)
    show_stat_info(port, tcp=False)

    s_data = 'Python zen.'
    udp_client_sock.sendto(s_data.encode(), ('127.0.0.1', port))
    print('sent data "%s" by udp endpoint.' % s_data)
    show_stat_info(port, tcp=False)

    r_data, __ = udp_server_sock.recvfrom(20)
    print('\nreceived data "%s", %d bytes from udp endpoint.' % (r_data, len(r_data)))
    show_stat_info(port, tcp=False)

    r_data, __ = udp_server_sock.recvfrom(5)
    print('received data "%s", %d bytes from udp endpoint.' % (r_data, len(r_data)))
    show_stat_info(port, tcp=False)

    udp_server_sock.setblocking(False)
    try:
        r_data, __ = udp_server_sock.recvfrom(5)
        print('received data "%s", %d bytes from udp endpoint.\n' % (r_data, len(r_data)))
        show_stat_info(port, tcp=False)
    except socket.error as e:
        if e.errno == errno.EAGAIN:
            print('no packet is ready.\n')

    tcp_server_sock.close()
    udp_server_sock.close()
    print('stop test server.')


if __name__ == '__main__':

    main()
