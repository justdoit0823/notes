
from tornado import httpserver, ioloop, web
from tornado.options import define, options, parse_command_line


class HelloWorldHandler(web.RequestHandler):
    """hello world handler."""

    output_str = 'hello world\n'

    def get(self):
        self.write(self.output_str)


def main():

    define('http_port', default='8787', help='http server port')
    define('http_host', default='', help='http server host')
    define('backlog', default=128, help='http server listen backlog')
    parse_command_line()

    app = web.Application([('/hello', HelloWorldHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.bind(
        options.http_port, address=options.http_host, backlog=options.backlog)
    http_server.start()
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':

    main()
