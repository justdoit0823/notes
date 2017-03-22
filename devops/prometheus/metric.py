
"""封装prometheus打点模块。"""

import functools
import socket

from prometheus_client import CollectorRegistry, Histogram, push_to_gateway
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop, PeriodicCallback


__all__ = ['register_metric_push', 'record_http_duration_metric']


_metric_registered = {}
_metric_host = socket.gethostname()

_collect_registry = CollectorRegistry()
_http_duration_buckets = (
    10, 20, 50, 80, 100, 200, 500, 1000, 3000, 5000, 10000)
_http_request_duration_microseconds = Histogram(
    'david_calendar_http_request_duration_microseconds',
    'HTTP request duration in microseconds.',
    labelnames=('host', 'method', 'url'),
    registry=_collect_registry, buckets=_http_duration_buckets)


def async_http_handler(url, method, timeout, headers, data):
    """HTTP handler base on tornado AsyncHTTPClient."""
    def handle():

        client = AsyncHTTPClient()
        future = client.fetch(
            url, method=method, headers=headers, connect_timeout=timeout,
            request_timeout=timeout, body=data)
        IOLoop.current().add_future(future, lambda f: f.result())

    return handle


def async_push_to_gateway(host, job, registry, grouping_key=None, timeout=None):
    """Push metrics to getway."""
    push_to_gateway(
        host, job, registry, grouping_key=grouping_key, timeout=timeout,
        handler=async_http_handler)


def register_metric_push(host, job, interval=15):

    key = '{0}-{1}'.format(host, job)
    if _metric_registered.get(key):
        return

    push_callback = functools.partial(
        async_push_to_gateway, host, job, _collect_registry, timeout=5)
    periodic_cb = PeriodicCallback(push_callback, interval * 1000)
    periodic_cb.start()

    key = '{0}-{1}'.format(host, job)
    _metric_registered[key] = True


def record_http_duration_metric(request):

    request_time = 1000.0 * request.request_time()
    _http_request_duration_microseconds.labels(
        host=_metric_host, method=request.method,
        url=request.path).observe(request_time)
