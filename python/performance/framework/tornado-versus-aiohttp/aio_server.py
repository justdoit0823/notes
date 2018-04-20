
"""A webserver based on aiohttp."""

from aiohttp import web


async def hello_handler(request):
    """Root handler."""
    return web.Response(text='Hello world.')


def main():
    app = web.Application()
    app.add_routes([
        web.get('/', hello_handler)
    ])

    web.run_app(app, host='127.0.0.1', port=8381)


if __name__ == '__main__':
    main()
