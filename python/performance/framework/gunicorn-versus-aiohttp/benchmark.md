
Benchmark
=========

Environment
-----------

  * ec2

`Linux localhost 4.14.12-x86_64-linode92 #1 SMP Fri Jan 5 15:34:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux`, 1G, 1C.

  * Python

`Python 3.6.2`.

  * framework

`aiohttp==3.1.3`, `gunicorn==19.7.1`.


Query
-----

```bash
wrk -c 128 -d 10s --latency server_api_url
```


Result
------

  * aiohttp server

```
Running 10s test @ http://127.0.0.1:8381/?duration=20
  2 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    52.56ms    3.22ms  86.00ms   88.86%
    Req/Sec     1.22k    97.14     1.29k    90.00%
  Latency Distribution
     50%   51.80ms
     75%   52.99ms
     90%   55.58ms
     99%   65.83ms
  24302 requests in 10.02s, 3.78MB read
Requests/sec:   2426.53
Transfer/sec:    386.25KB
```

Without delay,

```
Running 10s test @ http://127.0.0.1:8381/?duration=0
  2 threads and 128 connections

  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    49.03ms    3.26ms  77.02ms   93.22%
    Req/Sec     1.31k    98.52     1.50k    80.50%
  Latency Distribution
     50%   48.44ms
     75%   49.47ms
     90%   50.77ms
     99%   68.01ms
  26043 requests in 10.02s, 4.05MB read
Requests/sec:   2600.11
Transfer/sec:    413.90KB
```


  * gunicorn server

```
Running 10s test @ http://127.0.0.1:8380/?duration=20
  2 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    38.84ms    2.78ms  81.18ms   87.88%
    Req/Sec     1.65k   205.12     1.94k    67.00%
  Latency Distribution
     50%   38.26ms
     75%   39.49ms
     90%   41.38ms
     99%   47.04ms
  32937 requests in 10.02s, 5.12MB read
Requests/sec:   3286.10
Transfer/sec:    523.08KB
```

Without delay,

```
Running 10s test @ http://127.0.0.1:8380/?duration=0
  2 threads and 128 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    35.27ms    2.64ms  61.39ms   94.89%
    Req/Sec     1.82k   132.03     1.94k    88.50%
  Latency Distribution
     50%   34.83ms
     75%   35.71ms
     90%   36.60ms
     99%   50.25ms
  36228 requests in 10.02s, 5.63MB read
Requests/sec:   3616.67
Transfer/sec:    575.72KB
```
