
"""Test whether incomming conenction is balanced between listen queues."""

import os
import socket
import sys
import threading
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
    while num > 0:
        c_sock = socket.socket()
        c_sock.connect(('127.0.0.1', port))
        num -= 1
        con_cnt += 1

    print('already made %d conenctions.' % con_cnt)


def show_stat_info(port):
    cmd = 'ss -tnlp|grep 127.0.0.1:{0}'.format(port)
    os.system(cmd)


def main():
    if len(sys.argv) < 2:
        print('local server port is needed.')
        return

    port = int(sys.argv[1])

    server_sock_1 = bind_local_server(port)
    server_sock_2 = bind_local_server(port)

    make_connection(port)
    show_stat_info(port)

    pick_thread_1 = threading.Thread(
        target=pick_connection, args=(server_sock_1, 0))
    pick_thread_2 = threading.Thread(
        target=pick_connection, args=(server_sock_2, 1))

    pick_thread_1.start()
    pick_thread_2.start()

    pick_thread_1.join()
    pick_thread_2.join()

    server_sock_1.close()
    server_sock_2.close()
    print('stop first server.')
    

if __name__ == '__main__':

    main()
