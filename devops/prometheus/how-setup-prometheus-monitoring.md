
Prometheus
==========

[Prometheus](https://prometheus.io/docs/introduction/overview/) is an open-source systems monitoring and alerting toolkit originally built and written in Golang at SoundCloud.



Features
--------

  * a multi-dimensional data model (time series identified by metric name and key/value pairs)

  * a flexible query language to leverage this dimensionality

  * no reliance on distributed storage; single server nodes are autonomous

  * time series collection happens via a pull model over HTTP

  * pushing time series is supported via an intermediary gateway

  * targets are discovered via service discovery or static configuration

  * multiple modes of graphing and dashboarding support


Install
=======

Binary
------

Download binary from [download section](https://prometheus.io/download).


Docker
------

```
# Bind-mount your prometheus.yml from the host

docker run -p 9090:9090 -v /tmp/prometheus.yml:/etc/prometheus/prometheus.yml \
       prom/prometheus


# use an additional volume for the config

docker run -p 9090:9090 -v /prometheus-data \
       prom/prometheus -config.file=/prometheus-data/prometheus.yml
```

Using configuration management systems
--------------------------------------

### Ansible ###

  * [griggheo/ansible-prometheus](https://github.com/griggheo/ansible-prometheus)

  * [William-Yeh/ansible-prometheus](https://github.com/William-Yeh/ansible-prometheus)

### Chef ###

  * [rayrod2030/chef-prometheus](https://github.com/rayrod2030/chef-prometheus)


### SaltStack ###

  * [bechtoldt/saltstack-prometheus-formula](https://github.com/bechtoldt/saltstack-prometheus-formula)


Run
=====

Configure
---------

```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

```

Starting Prometheus
-------------------

```
./prometheus -config.file=prometheus.yml
```


Data Model
==========

Prometheus fundamentally stores all data as time series: streams of timestamped values belonging to the same metric and the same set of labeled dimensions.

```
Time Series 1
	|---- metric record(http_request_duration{method="GET", url="/api/index"} 50)
	|---- metric record(http_request_duration{method="GET", url="/api/config"} 60)
	|---- ...

Time Series 2
	|---- metric record(total_memory 1.2)
	|---- metric record(total_memory 1.3)
	|---- ...

```


Metric name and Labels
-------------------------

Every time series is uniquely identified by its metric name and a set of key-value pairs, also known as labels.


### Metric ###

The metric name specifies the general feature of a system that is measured.

It must match the regex [a-zA-Z_:][a-zA-Z0-9_:]*.


### Label ###

Labels enable Prometheus's dimensional data model.

They must match the regex [a-zA-Z_][a-zA-Z0-9_]*.


### Notation ###

```
<metric name>{<label name>=<label value>, ...}
```

Metric Type
-----------

### Counter ###

A counter is typically used to count requests served, tasks completed, errors occurred, etc.

Counters should not be used to expose current counts of items whose number can also go down.


### Gauge ###

A gauge is a metric that represents a single numerical value that can arbitrarily go up and down.

Gauges are typically used for measured values like temperatures or current memory usage,

but also "counts" that can go up and down, like the number of running goroutines.


### Hostogram ###

A histogram samples observations (usually things like request durations or response sizes) and counts them in configurable buckets.

It also provides a sum of all observed values.

A histogram with a base metric name of <basename> exposes multiple time series during a scrape:

  * cumulative counters for the observation buckets, exposed as <basename>_bucket{le="<upper inclusive bound>"}

  * the total sum of all observed values, exposed as <basename>_sum

  * the count of events that have been observed, exposed as <basename>\_count (identical to <basename>_bucket{le="+Inf"} above)


### Summary ###

Similar to a histogram, a summary samples observations (usually things like request durations and response sizes).

While it also provides a total count of observations and a sum of all observed values, it calculates configurable quantiles over a sliding time window.

A summary with a base metric name of <basename> exposes multiple time series during a scrape:

  * streaming φ-quantiles (0 ≤ φ ≤ 1) of observed events, exposed as <basename>{quantile="<φ>"}

  * the total sum of all observed values, exposed as <basename>_sum

  * the count of events that have been observed, exposed as <basename>_count



Architecture
============

![The architecture of Prometheus](https://prometheus.io/assets/architecture.svg)



Scrape Metric
=============


Job and Instance
------------------

### Job ###

Job is a collection of instances of the same type (replicated for scalability or reliability) .


### Instance ###

In Prometheus terms, any individually scraped target is called an instance, usually corresponding to a single process.

### Relation ###

```
job: api-server

	instance_1: 127.0.0.1:8081
	instance_2: 127.0.0.1:8082
	instance_3: 127.0.0.1:8083
	instance_4: 127.0.0.1:8084
```


Components
==========

  * the main Prometheus server which scrapes and stores time series data

  * client libraries for instrumenting application code

  * a push gateway for supporting short-lived jobs

  * a GUI-based dashboard builder based on Rails/SQL

  * special-purpose exporters (for HAProxy, StatsD, Graphite, etc.)

  * an (experimental) alertmanager

  * a command-line querying tool

  * various support tools


Record Metric In Python Project
===============================

Requirements
------------

  * [push gateway](https://github.com/prometheus/pushgateway)

  * [python client](https://github.com/prometheus/client_python)


Start push gateway
------------------

```
./pushgateway -web.listen-address ":9091"
```


Integration
-----------

### Tornado ###

```
import functools

from prometheus_client import CollectorRegistry, Histogram, push_to_gateway
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop, PeriodicCallback


_collect_registry = CollectorRegistry()
_http_duration_buckets = (
    10, 20, 50, 80, 100, 200, 500, 1000, 3000, 5000, 10000)
_http_request_duration_microseconds = Histogram(
	'http_request_duration_microseconds',
    'HTTP request duration in microseconds.',
    labelnames=('method', 'url'),
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
    """Push metrics to gateway."""
    push_to_gateway(
        host, job, registry, grouping_key=grouping_key, timeout=timeout,
        handler=async_http_handler)


def register_metric_push(host, job, interval=15):

	push_callback = functools.partial(
        async_push_to_gateway, host, job, _collect_registry, timeout=5)
    periodic_cb = PeriodicCallback(push_callback, interval * 1000)
    periodic_cb.start()


def record_http_duration_metric(request):

    request_time = 1000.0 * request.request_time()
    _http_request_duration_microseconds.labels(
        method=request.method, url=request.path).observe(request_time)

```


### Django ###

```
import functools
import time

from django.conf import settings
from django.core.signals import request_started, request_finished
from prometheus_client import CollectorRegistry, Histogram, push_to_gateway


_collect_registry = CollectorRegistry()
_http_duration_buckets = (
    10, 20, 50, 80, 100, 200, 500, 1000, 3000, 5000, 10000)
_http_request_duration_microseconds = Histogram(
	'http_request_duration_microseconds',
    'HTTP request duration in microseconds.',
    labelnames=('method', 'url'),
    registry=_collect_registry, buckets=_http_duration_buckets)


class RecordMetricMiddleware:

	def __init__(self):

	    self.register_metric_push(settings.PUSH_METRIC_INTERVAL)
		self._last_push_time = time.time()

	def register_metric_push(self, interval=15):

	    request_started.connect(self.push_metric)
		request_finished.connect(self.push_metric)

	def push_metric(self):

	    now = time.time()
		if now - self._last_push_time >= interval:
			push_to_gateway(
				settings.PUSH_METRIC_HOST, settings.PUSH_METRIC_JOB,
				_collect_registry)
			self._last_push_time = time.time()

	def process_request(self, request):

	    self._start_time = time.time()

	def process_response(self, request, response):

	    finish_time = time.time()
		duration = max(finish_time - self._start_time, 0)
		record_http_duration_metric(request, duration)


def record_http_duration_metric(request, duration):

	request_time = 1000.0 * duration
    _http_request_duration_microseconds.labels(
        method=request.method, url=request.path).observe(duration)

```


Visualization
===============

Open http://localhost:9090/ in web browser.



Advantage vs Disadvantage
==========================

When does it fit
-----------------

Prometheus works well for recording any purely numeric time series. It fits both machine-centric monitoring as well as monitoring of highly dynamic service-oriented architectures.

In a world of microservices, its support for multi-dimensional data collection and querying is a particular strength.

Prometheus is designed for reliability, to be the system you go to during an outage to allow you to quickly diagnose problems.

Each Prometheus server is standalone, not depending on network storage or other remote services.

You can rely on it when other parts of your infrastructure are broken, and you do not have to set up complex infrastructure to use it.


When does it not fit
--------------------

Prometheus values reliability. You can always view what statistics are available about your system, even under failure conditions.

If you need 100% accuracy, such as for per-request billing, Prometheus is not a good choice as the collected data will likely not be detailed and complete enough.

In such a case you would be best off using some other system to collect and analyse the data for billing, and Prometheus for the rest of your monitoring.


Reference
=========

  * <https://prometheus.io/docs/introduction/overview/>
