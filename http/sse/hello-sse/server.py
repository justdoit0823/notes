
"""Hello server send event module."""

import asyncio
import random
import string

import aiohttp
from aiohttp import web
import aiohttp_jinja2
from aiohttp_sse import sse_response
import click
import jinja2


_c_queue_mapping = {}
_shutdown_event = asyncio.Event()


def get_random_string(length):
    """Return fixed length string."""
    return ''.join(random.choice(string.ascii_letters) for idx in range(length))


async def _shutdown(*args):
    """Shutdown cleaner."""
    _shutdown_event.set()


@aiohttp_jinja2.template('index.html')
async def index_handler(request):
    token = get_random_string(32)
    return {'token': token}


async def sse_handler(request):
    try:
        token = request.query['token']
    except KeyError:
        return web.HTTPBadRequest()

    loop = request.app.loop
    try:
        c_queue = _c_queue_mapping[token]
    except KeyError:
        c_queue = asyncio.Queue()
        _c_queue_mapping[token] = c_queue

    async with sse_response(request) as resp:
        while not _shutdown_event.is_set():
            msg = await c_queue.get()
            await resp.send(msg)

    return resp


async def push_message_handler(request):
    """Push message to sse client."""
    token = request.query['token']
    body = request.query['body']

    try:
        c_queue = _c_queue_mapping[token]
    except KeyError:
        c_queue = asyncio.Queue()
        _c_queue_mapping[token] = c_queue

    await c_queue.put(body)

    return web.Response(text='ok')


@click.group()
def main():
    pass


@main.command('run', help='start websocket server.')
@click.argument('host', type=str, default='127.0.0.1')
@click.argument('port', type=str, default=8989)
def run(**kwargs):
    host = kwargs['host']
    port = kwargs['port']

    app = web.Application()
    app.add_routes([
        web.get('/', index_handler),
        web.get('/sse', sse_handler),
        web.get('/pub', push_message_handler)
    ])

    app.on_shutdown.append(_shutdown)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('.'))

    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    main()
