
"""Test coroutine reentrance in tornado."""

import functools
import random
import sys
import threading
import time

from tornado import gen, ioloop, httpclient, web

gen_user_set = set()
process_coroutine = set()
entry_coroutine = set()
ok_coroutine = set()


def process_user(io_loop, user_id):
    if user_id not in process_coroutine:
        process_coroutine.add(user_id)
    else:
        print('process reentrance user', user_id)

    future = push_user(user_id)
    io_loop.add_future(future, lambda f: f.result())


@gen.coroutine
def push_user(user_id):
    if user_id not in entry_coroutine:
        entry_coroutine.add(user_id)
    else:
        print('entry reentrance user', user_id)

    yield httpclient.AsyncHTTPClient().fetch('http://localhost/proxy.pac')

    if user_id not in ok_coroutine:
        ok_coroutine.add(user_id)
    else:
        print('reentrance user', user_id)


def generate_notice_message(stop_event, io_loop, rate):
    count = 0
    s_user_id = int(time.time() * 1000000)
    print('start user id', s_user_id)

    while not stop_event.is_set():
        user_id = s_user_id + random.choice(range(1, 5))
        if user_id not in gen_user_set:
            gen_user_set.add(user_id)
        else:
            print('gen deplicate user', user_id)

        def cb(user_id):
            process_user(io_loop, user_id)

        io_loop.add_callback(functools.partial(cb, user_id))
        count += 1

        time.sleep(1 / rate)
        s_user_id = user_id

    print('total user count %d.' % count)


def local_test_server():
    """Start local server."""
    class IndexHandler(web.RequestHandler):

        def get(self):
            yield gen.sleep(random.randint(20, 50) / 1000)
            self.write('Hello world.')


def main():
    """启动测试程序."""
    seconds = int(sys.argv[1])
    rate = int(sys.argv[2])

    stop_event = threading.Event()

    def stop_handler():
        io_loop.stop()
        stop_event.set()

    io_loop = ioloop.IOLoop.instance()
    io_loop.add_timeout(time.time() + seconds, stop_handler)

    generate_msg_thread = threading.Thread(
        target=generate_notice_message, args=(stop_event, io_loop, rate))
    generate_msg_thread.start()

    io_loop.start()

    generate_msg_thread.join()


if __name__ == '__main__':
    main()
