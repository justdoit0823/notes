
Benchmark
=========

Environment
-----------

  * ec2

`Linux localhost 4.14.12-x86_64-linode92 #1 SMP Fri Jan 5 15:34:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux`, 1G, 1C.

  * Python

`Python 3.6.2`.

  * framework

`aiohttp==3.1.3`, `sanic==0.7.0`.


Query
-----

```bash
wrk -c 64 -d 10s --latency server_api_url
```


Result
------

  * aio_server

```
Running 10s test @ http://127.0.0.1:8381
  2 threads and 64 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    19.64ms    1.49ms  48.07ms   93.99%
    Req/Sec     1.64k   123.71     1.92k    83.50%
  Latency Distribution
     50%   19.35ms
     75%   19.65ms
     90%   20.58ms
     99%   25.03ms
  32573 requests in 10.01s, 5.06MB read
Requests/sec:   3253.71
Transfer/sec:    517.94KB
```

  * aio_server(with uvloop)

```
Running 10s test @ http://127.0.0.1:8381
  2 threads and 64 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    13.41ms  690.69us  24.54ms   83.70%
    Req/Sec     2.40k   150.01     2.59k    41.50%
  Latency Distribution
     50%   13.33ms
     75%   13.78ms
     90%   14.05ms
     99%   15.62ms
  47715 requests in 10.01s, 7.42MB read
Requests/sec:   4765.10
Transfer/sec:    758.51KB
```

  * sanic

```
Running 10s test @ http://127.0.0.1:8382
  2 threads and 64 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    11.12ms  701.51us  22.00ms   95.52%
    Req/Sec     2.89k   140.71     3.23k    77.00%
  Latency Distribution
     50%   11.09ms
     75%   11.32ms
     90%   11.53ms
     99%   15.46ms
  57538 requests in 10.01s, 7.19MB read
Requests/sec:   5746.58
Transfer/sec:    735.16KB
```
