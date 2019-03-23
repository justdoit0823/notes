
import sys

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(sys.argv[1] if len(sys.argv) > 1 else '8081')
    tornado.ioloop.IOLoop.current().start()
