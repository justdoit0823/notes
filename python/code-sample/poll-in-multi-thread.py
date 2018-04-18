
import click
import select
import socket
import threading


@click.group()
def main():

    pass


@main.command('run_server')
@click.argument('host')
@click.argument('port')
def run(**kwargs):

    host = kwargs['host']
    port = int(kwargs['port'])
    s_sock = socket.socket()
    s_sock.bind((host, port))
    s_sock.listen(5)

    p_fd = select.poll()
    p_fd.register(s_sock.fileno(), select.POLLIN)

    thread1 = threading.Thread(target=poll, args=(p_fd,))
    thread2 = threading.Thread(target=poll, args=(p_fd,))

    thread1.start()
    thread2.start()


def poll(p_fd):

    while True:
        ret = p_fd.poll()
        print('return', ret, 'from poll')


if __name__ == '__main__':

    main()
