
"""Asynchronous connect."""

import errno
import select
import socket
import threading
import time


def local_server(addr, exit_event):
    s_socket = socket.socket()
    s_socket.bind(addr)
    s_socket.listen(5)

    s_socket.setblocking(False)

    clients = []

    while not exit_event.is_set():
        try:
            c_sock, __ = s_socket.accept()
        except OSError as e:
            if e.errno == errno.EAGAIN:
                time.sleep(0.2)
        else:
            clients.append(c_sock)

        for client in clients:
            try:
                print('receiving', client.recv(128))
            except OSError as e:
                if e.errno == errno.EAGAIN:
                    continue

    print('shutdown local server.')


def local_client(addr, exit_event):
    c_sock = socket.socket()
    c_sock.setblocking(False)

    try:
        c_sock.connect(addr)
    except BlockingIOError as e:
        if e.errno != errno.EINPROGRESS:
            raise

        print('connection in progress.')

        c_fd = c_sock.fileno()
        ep = select.poll()
        ep.register(c_fd, select.POLLOUT)

        while True:
            for fd, event in ep.poll(0.2):
                if fd == c_fd and event & select.POLLOUT == select.POLLOUT:
                    err_code = c_sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if err_code != 0:
                        raise ConnectionError(err_code)

                    break

            break

    c_sock.send(b'hello.')

    time.sleep(1)

    exit_event.set()
    print('close client.')


def main():
    port = 12345
    addr = ('127.0.0.1', port)
    exit_event = threading.Event()

    server_thread = threading.Thread(
        target=local_server, args=(addr, exit_event))
    server_thread.start()

    try:
        local_client(addr, exit_event)
    finally:
        exit_event.set()
        server_thread.join()


if __name__ == '__main__':
    main()
