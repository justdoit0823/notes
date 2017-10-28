
import pytest
from pytest_localserver.http import WSGIServer


def app(environ, start_response):
    """A simple WSGI application"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [environ['PATH_INFO'].encode()]


@pytest.fixture(scope='module')
def testserver():
    """Define the test WSGI server."""
    server = WSGIServer(host='127.0.0.1', port=8031, application=app)
    server.start()
    yield server
    server.stop()
