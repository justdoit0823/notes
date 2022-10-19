"""Show Recv-Q value with udp protocol in ss."""

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

    # cmd = cmd + "|awk '$4 == \"127.0.0.1:{0}\"'".format(port)
    cmd = cmd + "|grep 127.0.0.1:{0}".format(port)

    if gt_zero:
        cmd = cmd + "|awk '$2 > 0'"

    os.system(cmd)
    # if not tcp:
    #     os.system('cat /proc/net/dev')


def main():
    if len(sys.argv) < 2:
        print('local server port is needed.')
        return

    port = int(sys.argv[1])
    # num = int(sys.argv[2])
    num = 5

    udp_server_sock = bind_local_udp_server(port)

    udp_client_sock = socket.socket(type=socket.SOCK_DGRAM)
    udp_client_sock.connect(('127.0.0.1', port))

    for i in range(num):
        s_data = 'H' * (1 + 100 * i)
        udp_client_sock.sendto(s_data.encode(), ('127.0.0.1', port))
        print('sent %d bytes data by udp endpoint.' % len(s_data))
        show_stat_info(port, tcp=False)

    # s_data = 'P'
    # udp_client_sock.sendto(s_data.encode(), ('127.0.0.1', port))
    # print('sent %d bytes data by udp endpoint.' % len(s_data))
    # show_stat_info(port, tcp=False)

    # s_data = 'P' * 100
    # udp_client_sock.sendto(s_data.encode(), ('127.0.0.1', port))
    # print('sent %d bytes data by udp endpoint.' % len(s_data))
    # show_stat_info(port, tcp=False)

    udp_server_sock.close()
    print('stop test server.')


if __name__ == '__main__':

    main()