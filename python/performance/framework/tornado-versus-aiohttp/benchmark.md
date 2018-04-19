
Benchmark
=========

Environment
-----------

  * ec2

`Linux localhost 4.14.12-x86_64-linode92 #1 SMP Fri Jan 5 15:34:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux`, 1G, 1C.

  * Python

`Python 3.6.2`.

  * framework

`tornado==5.0.2`, `aiohttp==3.1.3`.


Query
-----

```bash
wrk -c 128 -d 10s --latency server_api_url
```


Result
------

  * aio server

```
Running 10s test @ http://127.0.0.1:8381/
  2 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    44.02ms    1.70ms  51.90ms   85.43%
    Req/Sec     1.46k   157.50     1.86k    46.50%
  Latency Distribution
     50%   43.89ms
     75%   44.61ms
     90%   45.55ms
     99%   49.84ms
  29012 requests in 10.01s, 4.51MB read
Requests/sec:   2898.23
Transfer/sec:    461.35KB
```

  * tornado server

```
Running 10s test @ http://127.0.0.1:8382/
  2 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    88.22ms   15.62ms 407.19ms   98.75%
    Req/Sec   729.74     88.70     1.00k    52.50%
  Latency Distribution
     50%   87.69ms
     75%   88.46ms
     90%   89.31ms
     99%   98.89ms
  14535 requests in 10.01s, 2.87MB read
Requests/sec:   1451.51
Transfer/sec:    293.42KB
```
