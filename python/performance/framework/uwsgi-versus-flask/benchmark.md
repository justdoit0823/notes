
Benchmark
=========

Environment
-----------

  * ec2

`Linux localhost 4.14.12-x86_64-linode92 #1 SMP Fri Jan 5 15:34:44 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux`, 1G, 1C.

  * Python

`Python 3.6.2`.

  * framework

`flask==0.12.2`, `uwsgi==2.0.17`.


Query
-----

```bash
wrk -c 16 -d 10s --latency server_api_url
```


Result
------

  * flask server

```
Running 10s test @ http://127.0.0.1:5000/
  2 threads and 16 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    14.38ms    1.12ms  27.84ms   95.08%
    Req/Sec   556.38     21.53   590.00     79.00%
  Latency Distribution
     50%   14.19ms
     75%   14.51ms
     90%   15.00ms
     99%   19.86ms
  11085 requests in 10.01s, 1.75MB read
Requests/sec:   1107.59
Transfer/sec:    179.55KB
```

  * uwsgi server

```
Running 10s test @ http://127.0.0.1:9090/
  2 threads and 16 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.41ms  743.43us  15.05ms   90.91%
    Req/Sec     1.24k    45.10     1.32k    73.50%
  Latency Distribution
     50%    6.27ms
     75%    6.59ms
     90%    7.02ms
     99%    9.95ms
  24613 requests in 10.01s, 2.14MB read
  Socket errors: connect 0, read 24611, write 0, timeout 0
Requests/sec:   2459.20
Transfer/sec:    218.54KB
```
