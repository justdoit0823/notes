"""A webserver based on aiohttp."""

import argparse
import asyncio

import aiohttp
from aiohttp import web
import uvloop


async def hello_handler(request):
    """Root handler."""
    return web.Response(text='Hello world.')


def main():
    parser = argparse.ArgumentParser(
        description='A webserver based on aiohttp.')
    parser.add_argument(
        '--uvloop', dest='uvloop', action='store_const', const=True,
        help='use uvloop.')
    args = parser.parse_args()

    app = web.Application()
    app.add_routes([
        web.get('/', hello_handler)
    ])

    if args.uvloop:
        print('running the uvloop...')
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    web.run_app(app, host='127.0.0.1', port=8381, backlog=1024)


if __name__ == '__main__':
    main()