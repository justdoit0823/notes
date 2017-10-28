
import requests

url = 'http://127.0.0.1:8031'


class TestFooGroup:

    def test_foo_a(self, testserver):
        res = requests.get(url + '/foo/a')
        assert res.content.decode() == '/foo/a'

    def test_foo_b(self, testserver):
        res = requests.get(url + '/foo/b')
        assert res.content.decode() == '/foo/b'


class TestBarGroup:

    def test_bar_a(self, testserver):
        res = requests.get(url + '/bar/a')
        assert res.content.decode() == '/bar/a'

    def test_bar_b(self, testserver):
        res = requests.get(url + '/bar/b')
        assert res.content.decode() == '/bar/b'
