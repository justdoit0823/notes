
"""A tornado web server."""

from tornado import httpserver, ioloop, web


class IndexHandler(web.RequestHandler):
    """Index handler."""

    def get(self):
        self.write('Hello world.')


def main():
    app = web.Application([
        (r'/', IndexHandler)
    ])

    server = httpserver.HTTPServer(app)
    server.bind(8382, '127.0.0.1')
    server.start()

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
