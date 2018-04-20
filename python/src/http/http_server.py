
"""A web server based on standard http libary."""

from http import server


class HTTPRequestHandler(server.BaseHTTPRequestHandler):
    """Hello world http request handler."""

    def do_GET(self):
        """Handle GET request."""
        self.send_response(server.HTTPStatus.OK)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello world.')


def main():
    http_server = server.HTTPServer(('127.0.0.1', 8384), HTTPRequestHandler)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
