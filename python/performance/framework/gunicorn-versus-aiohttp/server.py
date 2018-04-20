
"""A webserver based on aiohttp."""

import asyncio

from aiohttp import web


async def hello_handler(request):
    """Root handler."""
    try:
        duration = int(request.query['duration'])
    except (KeyError, ValueError):
        duration = 0

    if duration:
        await asyncio.sleep(duration / 1000)

    return web.Response(text='Hello world.')


app = web.Application()
app.add_routes([
    web.get('/', hello_handler)
])


def main():
    web.run_app(app, host='127.0.0.1', port=8381)


if __name__ == '__main__':
    main()
