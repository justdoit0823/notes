
How to write a file?
=====================

In linux operating system, there is a [posix](https://en.wikipedia.org/wiki/POSIX) api `write`, which supports writing `count` bytes to a file.
Before writing, we need a file descriptor which can be returned from another posix api `open`.
But how could we operate in python?

we can refer such apis from `os` module, which includes all functions from posix. For example,

```python
import os

fd = os.open('/tmp/test_os_module', os.O_WRONLY)
data = b'test os module.'
count = os.write(fd, data)
print(count, 'bytes data has been written.')
os.close(fd)
```

It's quite similar to how we write with `open`, `write` and `close` apis in c. Right?
According to python's execution speed, these operations run slower than c? Probably yes, but I need a benchmark.


Writing benchmark
=================

In order to comparing writing speed between python and c, I have written two programs in python and c.
All programs can be found at <https://github.com/justdoit0823/notes/tree/master/python/code-sample/how-the-write-function-in-python-runs-as-fast-as-that-in-c>.


Asynchronous write
------------------

### Test on macOS ###

Firstly, I ran the benchmark on my MacBook Pro. And the system info is `Darwin yusenbindeMacBook-Pro.local 17.2.0 Darwin Kernel Version 17.2.0: Fri Sep 29 18:27:05 PDT 2017; root:xnu-4570.20.62~3/RELEASE_X86_64 x86_64`.


  * C version

Test bash script,

```bash
for i in `seq 5`; do time ./disk-io-benchmark 10737418240 4096; done
```

The test output,

```
write to temp file /tmp/disk-io-TiW39H .
successfully write 10737418240 bytes.

real	0m24.368s
user	0m0.344s
sys	0m20.290s
write to temp file /tmp/disk-io-womWA6 .
successfully write 10737418240 bytes.

real	0m26.616s
user	0m0.367s
sys	0m21.952s
write to temp file /tmp/disk-io-TLo3WO .
successfully write 10737418240 bytes.

real	0m26.661s
user	0m0.367s
sys	0m22.137s
write to temp file /tmp/disk-io-LPU4sr .
successfully write 10737418240 bytes.

real	0m25.504s
user	0m0.364s
sys	0m21.311s
write to temp file /tmp/disk-io-NzMOYp .
successfully write 10737418240 bytes.

real	0m25.627s
user	0m0.357s
sys	0m21.333s
```

The disk io statistic,

```
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   63.62 7260 451.00   2 38 60  2.13 1.76 1.69
   63.80 7191 448.03   3 39 58  2.36 1.81 1.71
   63.81 7013 437.01   1 38 61  2.36 1.81 1.71
   63.78 7029 437.77   2 39 58  2.36 1.81 1.71
   63.79 6838 425.98   4 39 56  2.36 1.81 1.71
   63.72 6846 425.99   3 38 59  2.36 1.81 1.71
   63.75 6779 422.04   2 41 57  2.49 1.85 1.72
   63.70 6691 416.24   4 39 57  2.49 1.85 1.72
   63.50 6452 400.10   8 40 52  2.49 1.85 1.72
   63.53 3570 221.50   4 35 61  2.49 1.85 1.72
   63.68 5222 324.71   7 38 55  2.49 1.85 1.72
   63.77 6337 394.69   8 40 52  2.37 1.83 1.71
   63.59 6679 414.75   4 40 56  2.37 1.83 1.71
   63.57 6082 377.53  13 42 46  2.37 1.83 1.71
   63.29 6621 409.21   4 39 57  2.37 1.83 1.71
   63.78 6441 401.14   6 41 53  2.37 1.83 1.71
   63.78 6671 415.52   4 40 56  2.42 1.85 1.72
   63.77 5967 371.55  12 40 48  2.42 1.85 1.72
   63.75 6011 374.17  11 40 49  2.42 1.85 1.72
   63.56 6201 384.88   9 40 52  2.42 1.85 1.72
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   63.48 5957 369.28   8 43 49  2.42 1.85 1.72
   63.77 6489 404.08   5 40 55  2.47 1.87 1.73
   63.77 6243 388.75   7 40 52  2.47 1.87 1.73
   63.69 6341 394.37   7 40 53  2.47 1.87 1.73
   63.75 6348 395.21   7 40 53  2.47 1.87 1.73
   62.59 6660 407.06   5 41 54  2.47 1.87 1.73
   63.65 6448 400.80   6 40 54  2.59 1.90 1.74
   63.72 6243 388.51   6 40 54  2.59 1.90 1.74
   63.75 6513 405.44   5 40 55  2.59 1.90 1.74
   63.64 6168 383.35   8 41 51  2.59 1.90 1.74
   63.75 6174 384.32   7 41 53  2.59 1.90 1.74
   63.72 6122 380.97   7 40 54  2.62 1.92 1.75
   63.73 6597 410.58   4 40 56  2.62 1.92 1.75
   63.77 6032 375.64  11 40 49  2.62 1.92 1.75
   63.56 6616 410.66   6 38 56  2.62 1.92 1.75
   63.85 5313 331.30   4 37 59  2.62 1.92 1.75
   63.55 3917 243.09   5 34 61  2.81 1.97 1.77
   63.75 6657 414.44   3 39 58  2.81 1.97 1.77
   63.72 6536 406.73   6 41 53  2.81 1.97 1.77
   63.81 6409 399.36   6 40 53  2.81 1.97 1.77
```

Obviously, the fastest writing speed is at `451 MB/s`, and the most of cpu time is spent in kernel context.


  * Python version

The test python info is `Python 3.6.0 [GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)]`.

The test bash script,

```
for i in `seq 5`; do time python disk-io-benchmark.py 10737418240 4096; done
```

Test output,

```
successfully write 10737418240 bytes.

real	0m26.430s
user	0m1.879s
sys	0m20.932s
successfully write 10737418240 bytes.

real	0m26.860s
user	0m1.960s
sys	0m21.113s
successfully write 10737418240 bytes.

real	0m25.659s
user	0m1.775s
sys	0m20.498s
successfully write 10737418240 bytes.

real	0m25.042s
user	0m1.813s
sys	0m19.902s
successfully write 10737418240 bytes.

real	0m25.783s
user	0m1.923s
sys	0m20.506s
```

The disk io statistic,

```
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   63.61 4074 253.07   4 31 65  3.38 2.43 2.11
   63.36 4578 283.29   2 33 65  3.51 2.48 2.13
   63.79 6615 412.05   2 36 62  3.51 2.48 2.13
   63.76 6593 410.48   2 36 62  3.51 2.48 2.13
   63.77 6512 405.51   2 35 62  3.51 2.48 2.13
   63.70 6540 406.86   2 35 63  3.51 2.48 2.13
   63.71 6626 412.26   2 36 62  3.71 2.53 2.15
   63.72 6792 422.69   2 36 62  3.71 2.53 2.15
   63.73 6791 422.61   2 36 62  3.71 2.53 2.15
   63.75 6769 421.41   2 36 62  3.71 2.53 2.15
   63.76 6720 418.47   3 36 62  3.71 2.53 2.15
   63.77 6782 422.33   2 36 62  3.57 2.52 2.15
   63.76 6755 420.61   2 36 62  3.57 2.52 2.15
   63.47 6791 420.94   2 35 62  3.57 2.52 2.15
   63.76 6737 419.49   2 35 62  3.57 2.52 2.15
   63.70 6488 403.61   6 36 58  3.57 2.52 2.15
   63.34 6812 421.33   2 36 61  3.69 2.56 2.17
   63.55 6867 426.15   2 36 62  3.69 2.56 2.17
   63.65 6762 420.33   3 36 61  3.69 2.56 2.17
   62.93 6471 397.72   2 37 61  3.69 2.56 2.17
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   63.76 6791 422.86   2 36 62  3.69 2.56 2.17
   63.74 6806 423.66   2 36 62  3.55 2.56 2.17
   63.77 6822 424.84   2 36 62  3.55 2.56 2.17
   63.76 6816 424.39   2 36 62  3.55 2.56 2.17
   63.74 6830 425.12   3 35 62  3.55 2.56 2.17
   63.48 5676 351.87   4 34 63  3.55 2.56 2.17
   63.35 4550 281.48   2 32 66  3.67 2.60 2.18
   63.76 6647 413.90   2 36 62  3.67 2.60 2.18
   63.76 6515 405.66   3 36 62  3.67 2.60 2.18
   63.76 6505 405.03   2 35 63  3.67 2.60 2.18
   63.73 6452 401.52   3 35 62  3.67 2.60 2.18
   63.74 6365 396.22   2 36 62  3.77 2.64 2.20
   63.73 6470 402.68   2 35 63  3.77 2.64 2.20
   63.75 6467 402.65   2 35 62  3.77 2.64 2.20
   63.77 6672 415.50   2 35 62  3.77 2.64 2.20
   63.74 6697 416.92   2 35 63  3.77 2.64 2.20
   63.74 6616 411.79   2 36 62  3.63 2.62 2.20
   63.73 6424 399.79   7 35 58  3.63 2.62 2.20
   63.75 6595 410.56   2 36 62  3.63 2.62 2.20
   63.78 6625 412.64   2 35 63  3.63 2.62 2.20
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   63.66 6435 400.06   7 36 57  3.63 2.62 2.20
   63.64 6690 415.79   3 35 62  3.50 2.61 2.20
   63.63 6594 409.72   3 35 62  3.50 2.61 2.20
   63.69 6696 416.52   3 35 62  3.50 2.61 2.20
   63.67 6709 417.21   2 36 62  3.50 2.61 2.20
   63.78 6683 416.25   2 35 63  3.50 2.61 2.20
   63.75 6703 417.32   3 35 62  3.62 2.65 2.21
   63.72 6675 415.35   2 36 62  3.62 2.65 2.21
   63.73 6692 416.44   2 35 63  3.62 2.65 2.21
   63.20 6153 379.77   3 38 59  3.62 2.65 2.21
   63.74 6564 408.63   2 35 62  3.62 2.65 2.21
   64.00 1706 106.61   3 16 81  3.49 2.64 2.21
   22.69   61  1.35   3  2 95  3.49 2.64 2.21
    0.00    0  0.00   1  1 98  3.49 2.64 2.21
```

I will discuss more details later.


### Test on ubuntu ###

Next, I ran the benchmark on my ubuntu server. And the system info is `Linux justdoit-thinkpad-e420 4.13.0-16-lowlatency #19-Ubuntu SMP PREEMPT Wed Oct 11 19:51:52 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux`.

  * C version

Test bash script,

```bash
for i in `seq 5`; do time ./disk-io-benchmark 1073741824 4096; done
```

The test output,

```
write to temp file /tmp/disk-io-18DaYE .
successfully write 1073741824 bytes.

real	0m6.035s
user	0m0.032s
sys	0m2.300s
write to temp file /tmp/disk-io-mloPrX .
successfully write 1073741824 bytes.

real	0m14.633s
user	0m0.049s
sys	0m3.111s
write to temp file /tmp/disk-io-nkibjd .
successfully write 1073741824 bytes.

real	0m13.750s
user	0m0.041s
sys	0m3.059s
write to temp file /tmp/disk-io-oMGjPZ .
successfully write 1073741824 bytes.

real	0m20.338s
user	0m0.047s
sys	0m3.145s
write to temp file /tmp/disk-io-lPDbwO .
successfully write 1073741824 bytes.

real	0m19.441s
user	0m0.051s
sys	0m3.110s
```

And the disk io statistic,

```
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.52    0.00   16.96   26.08    0.00   55.44

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r\_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              2.00   80.00      8.00  79880.00     0.00     0.00   0.00   0.00  173.00  297.65  96.80     4.00   998.50  12.20 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.01    0.00   14.32   32.91    0.00   51.76

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00   76.00    132.00  76800.00    31.00   109.00  96.88  58.92  132.00 1164.08 141.94   132.00  1010.53  12.99 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.28    0.00   11.22   36.99    0.00   50.51

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00   95.00      4.00  82896.00     0.00   196.00   0.00  67.35  111.00 1737.78 142.09     4.00   872.59  10.42 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.01    0.00    9.85   50.00    0.00   39.14

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00   94.00      4.00  80204.00     0.00    57.00   0.00  37.75   20.00 1498.33 136.61     4.00   853.23  10.54 100.10
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.53    0.00    8.40   47.07    0.00   43.00

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00  108.00      4.00  77824.00     0.00   105.00   0.00  49.30  118.00 1393.14 144.32     4.00   720.59   9.17 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    7.12   44.02    0.00   47.58

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00   89.00      4.00  82500.00     0.00     7.00   0.00   7.29  159.00 1342.37 141.91     4.00   926.97  11.11 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.79    0.00    8.42   46.17    0.00   43.62

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  102.00      0.00  81504.00     0.00   146.00   0.00  58.87    0.00 1536.15 143.00     0.00   799.06   9.80 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    6.62   56.49    0.00   35.62

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  115.00      0.00  81920.00     0.00    29.00   0.00  20.14    0.00 1329.62 142.23     0.00   712.35   8.70 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.53    0.00    7.89   46.31    0.00   44.27

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  126.00      0.00  82040.00     0.00   121.00   0.00  48.99    0.00 1214.90 142.17     0.00   651.11   7.94 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.02    0.00    7.89   47.07    0.00   44.02

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  104.00      0.00  81376.00     0.00    41.00   0.00  28.28    0.00 1227.31 143.98     0.00   782.46   9.62 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.78    0.00    6.85   67.01    0.00   24.37

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda             43.00   66.00   1460.00  50696.00     0.00   117.00   0.00  63.93   56.95 1610.56 145.25    33.95   768.12   9.17 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    6.33   49.87    0.00   42.53

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  114.00      0.00  82592.00     0.00    78.00   0.00  40.62    0.00 1568.56 142.75     0.00   724.49   8.77 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.53    0.00    8.14   48.85    0.00   41.48

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   99.00      0.00  82720.00     0.00   111.00   0.00  52.86    0.00 1324.80 144.27     0.00   835.56  10.10 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    8.04   59.55    0.00   31.16

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   62.00      0.00  51260.00     0.00   252.00   0.00  80.25    0.00 1766.92 136.77     0.00   826.77  16.13 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    7.58   42.17    0.00   48.99

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   93.00      0.00  82328.00     0.00     5.00   0.00   5.10    0.00 1812.88 138.84     0.00   885.25  10.76 100.10
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.01    0.00    7.85   56.71    0.00   34.43

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   98.00      0.00  82172.00     0.00   145.00   0.00  59.67    0.00 1437.00 141.73     0.00   838.49  10.19  99.90
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    8.33   61.62    0.00   28.79

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00   92.00      4.00  79876.00     0.00   144.00   0.00  61.02  313.00 1543.58 143.58     4.00   868.22  10.75 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.01    0.00    5.81   79.55    0.00   13.64

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda            104.95   78.22    598.02  69972.28    44.55   349.50  29.80  81.71   17.05 1485.25 144.79     5.70   894.58   5.41  99.11
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    7.89   50.64    0.00   40.20

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda             85.00   97.00    820.00  69632.00    72.00   195.00  45.86  66.78    7.28 1746.28 143.77     9.65   717.86   5.49 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    7.85   50.13    0.00   40.76

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  130.00      0.00  84064.00     0.00     2.00   0.00   1.52    0.00 1333.30 142.47     0.00   646.65   7.69 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.52    0.00    7.85   49.62    0.00   41.01

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  121.00      0.00  82000.00     0.00    20.00   0.00  14.18    0.00 1153.20 142.23     0.00   677.69   8.26 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.02    0.00    8.65   51.15    0.00   39.19

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   93.00      0.00  81920.00     0.00   101.00   0.00  52.06    0.00 1255.01 142.55     0.00   880.86  10.75 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.52    0.00    8.38   48.22    0.00   41.88

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              2.00   85.00      8.00  80288.00     0.00   147.00   0.00  63.36  234.50 1506.94 127.13     4.00   944.56  11.49 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.01    0.00    7.07   61.62    0.00   30.30

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   81.00      0.00  78848.00     0.00    47.00   0.00  36.72    0.00 1738.85 142.67     0.00   973.43  12.35 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.78    0.00    7.11   60.66    0.00   30.46

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   90.00      0.00  81736.00     0.00    12.00   0.00  11.76    0.00 1488.00 143.69     0.00   908.18  11.11 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    7.07   52.27    0.00   39.39

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   83.00      0.00  71680.00     0.00   184.00   0.00  68.91    0.00 1671.72 141.64     0.00   863.61  12.05 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.77    0.00    6.84   57.47    0.00   33.92

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   81.00      0.00  67544.00     0.00    60.00   0.00  42.55    0.00 1720.56 145.48     0.00   833.88  12.35 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    6.84   49.87    0.00   42.03

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   96.00      0.00  82944.00     0.00    50.00   0.00  34.25    0.00 1692.79 144.01     0.00   864.00  10.42 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.27    0.00    8.38   45.69    0.00   44.67

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  104.00      0.00  79052.00     0.00    49.00   0.00  32.03    0.00 1466.30 142.81     0.00   760.12   9.62 100.10
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
```

And the fastest writing speed is at `82MB/s`. From document of the command `iostat`, the `%util` value is explained as the followed.

>%util
>                     Percentage of elapsed time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs  when  this
>                     value is close to 100% for devices serving requests serially.  But for devices serving requests in parallel, such as RAID arrays and modern SSDs, this num‐
>                     ber does not reflect their performance limits.

So the disk's writing speed is saturated.


  * Python version

The python info is `Python 3.6.3 [GCC 7.2.0]`.

Test bash script,

```bash
for i in `seq 5`; do time python disk-io-benchmark.py 10737418240 4096; done
```

Test output,

```
successfully write 1073741824 bytes.

real	0m8.447s
user	0m0.582s
sys	0m2.543s
successfully write 1073741824 bytes.

real	0m13.885s
user	0m0.786s
sys	0m3.307s
successfully write 1073741824 bytes.

real	0m14.773s
user	0m0.829s
sys	0m3.466s
successfully write 1073741824 bytes.

real	0m19.497s
user	0m0.871s
sys	0m3.155s
successfully write 1073741824 bytes.

real	0m12.824s
user	0m0.728s
sys	0m3.240s
```

The disk io statistic,


```
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.28    0.00    8.35   50.13    0.00   39.24

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r\_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   92.00      0.00  81920.00     0.00     3.00   0.00   3.16    0.00 1451.10 143.09     0.00   890.43  10.87 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.77    0.00    5.79   44.08    0.00   47.36

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   95.00      0.00  82032.00     0.00     4.00   0.00   4.04    0.00 1471.36 142.89     0.00   863.49  10.53 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           3.03    0.00    9.85   42.42    0.00   44.70

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              1.00  108.00     12.00  79520.00     0.00    33.00   0.00  23.40  426.00 1520.07 140.81    12.00   736.30   9.17 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.02    0.00    5.81   49.49    0.00   42.68

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   71.00      0.00  63064.00     0.00    27.00   0.00  27.55    0.00 1540.03 139.68     0.00   888.23  14.08 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.53    0.00    7.59   62.28    0.00   27.59

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  102.00      0.00  83992.00     0.00     6.00   0.00   5.56    0.00 1565.57 143.81     0.00   823.45   9.80 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.52    0.00    8.31   59.45    0.00   29.72

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   99.00      0.00  82992.00     0.00    21.00   0.00  17.50    0.00 1424.99 142.48     0.00   838.30  10.10 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.27    0.00    8.56   44.08    0.00   45.09

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  100.00      0.00  83080.00     0.00    18.00   0.00  15.25    0.00 1444.76 141.56     0.00   830.80  10.00 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.53    0.00    7.09   46.08    0.00   44.30

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  101.00      0.00  83968.00     0.00     2.00   0.00   1.94    0.00 1423.60 141.99     0.00   831.37   9.90 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.53    0.00    9.34   53.03    0.00   35.10

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda             20.00   86.00    476.00  73732.00     0.00    16.00   0.00  15.69   53.30 1479.86 145.88    23.80   857.35   9.43 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.28    0.00    7.11   49.49    0.00   41.12

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   93.00      0.00  82048.00     0.00    17.00   0.00  15.45    0.00 1569.44 143.26     0.00   882.24  10.75 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.28    0.00    9.62   47.34    0.00   40.76

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   91.00      0.00  82948.00     0.00    51.00   0.00  35.92    0.00 1569.78 142.82     0.00   911.52  10.99 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.28    0.00    9.37   46.84    0.00   41.52

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00  111.00      0.00  82384.00     0.00    65.00   0.00  36.93    0.00 1471.31 142.79     0.00   742.20   9.01 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.54    0.00    7.61   50.76    0.00   39.09

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   96.00      0.00  82952.00     0.00     8.00   0.00   7.69    0.00 1397.11 143.76     0.00   864.08  10.42 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.28    0.00   10.38   52.41    0.00   34.94

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   92.00      0.00  82944.00     0.00    44.00   0.00  32.35    0.00 1463.25 142.46     0.00   901.57  10.87 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           2.03    0.00    5.82   52.41    0.00   39.75

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              5.00   93.00     56.00  76844.00     0.00    41.00   0.00  30.60  163.40 1551.13 143.12    11.20   826.28  10.21 100.10
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.00    0.00    2.26   40.10    0.00   56.64

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   84.00      0.00  65876.00     0.00     1.00   0.00   1.18    0.00 1472.27 144.85     0.00   784.24  11.90 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.51    0.00    2.26   31.66    0.00   64.57

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00   97.00      0.00  78580.00     0.00    21.00   0.00  17.80    0.00 1689.61 139.01     0.00   810.10  10.31 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    1.26   18.84    0.00   78.64

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              4.00   92.00     56.00  78180.00     0.00     0.00   0.00   0.00  172.50 1546.30  87.33    14.00   849.78  10.42 100.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.26    0.00    1.01   22.47    0.00   75.25

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda             23.00   42.00    380.00  36868.00     0.00     0.00   0.00   0.00   39.35 1588.19  16.70    16.52   877.81  11.31  73.50
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.00    0.00    0.25    0.00    0.00   98.75

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
sda              0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
scd0             0.00    0.00      0.00      0.00     0.00     0.00   0.00   0.00    0.00    0.00   0.00     0.00     0.00   0.00   0.00
```

To compare the results of these two versions, it's clear that the writing speed in python is almost similar to that in c.
This may be surprising to some of you, as the c program is far faster than python program. However here they are both limited to the disk's speed.


Synchronous write
-----------------

Out of curiosity, I tested the synchronous write speed. The following is test bash script.

```bash
for i in `seq 5`; do time ./disk-io-benchmark 1073741824 4096 1; done
```

The test output,

```
write to temp file /tmp/disk-io-B7Czy0 .
successfully write 1073741824 bytes.

real	0m20.787s
user	0m0.075s
sys	0m12.432s
write to temp file /tmp/disk-io-3hgLlw .
successfully write 1073741824 bytes.

real	0m19.130s
user	0m0.067s
sys	0m11.469s
write to temp file /tmp/disk-io-mg6IQv .
successfully write 1073741824 bytes.

real	0m18.813s
user	0m0.064s
sys	0m11.221s
write to temp file /tmp/disk-io-qyPr7o .
successfully write 1073741824 bytes.

real	0m19.285s
user	0m0.069s
sys	0m11.543s
write to temp file /tmp/disk-io-alIXsf .
successfully write 1073741824 bytes.

real	0m18.524s
user	0m0.062s
sys	0m11.015s
```


The disk io statistic,

```
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
   52.97    4  0.22   7  5 88  0.97 1.68 2.28
    0.00    0  0.00   7  4 90  0.97 1.68 2.28
    4.04 8765 34.59  13 23 63  0.97 1.68 2.28
    4.00 13764 53.77   6 24 71  0.97 1.68 2.28
    4.00 14178 55.38   5 24 71  0.97 1.68 2.28
    4.00 13854 54.12   7 25 68  0.97 1.67 2.27
    4.00 14360 56.10   5 24 71  0.97 1.67 2.27
    4.00 14699 57.42   3 23 74  0.97 1.67 2.27
    4.00 14460 56.55   3 23 74  0.97 1.67 2.27
    4.00 14795 57.79   3 23 74  0.97 1.67 2.27
    4.00 14465 56.51   5 24 72  0.97 1.66 2.27
    4.00 14533 56.77   5 23 72  0.97 1.66 2.27
    4.00 14231 55.59   6 24 70  0.97 1.66 2.27
    4.00 11833 46.22  20 28 52  0.97 1.66 2.27
    5.17 7464 37.68  26 33 41  0.97 1.66 2.27
    4.00 7619 29.78  23 31 46  1.13 1.68 2.27
    4.00 8642 33.76  18 29 53  1.13 1.68 2.27
    4.01 7471 29.25  24 31 44  1.13 1.68 2.27
    4.00 13963 54.60   6 24 70  1.13 1.68 2.27
    4.00 13723 53.61   6 25 68  1.13 1.68 2.27
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
    4.06 14031 55.63   7 24 70  1.12 1.67 2.26
    4.13 13365 53.91   6 28 66  1.12 1.67 2.26
    4.04 13022 51.43   6 25 68  1.12 1.67 2.26
    4.02 9595 37.70   5 26 69  1.12 1.67 2.26
    4.00 13979 54.61   5 25 70  1.12 1.67 2.26
    4.00 13997 54.67   6 26 68  1.11 1.66 2.25
    4.00 13612 53.17   8 26 65  1.11 1.66 2.25
    4.00 14052 54.89   5 26 69  1.11 1.66 2.25
    4.00 13246 51.80  10 26 64  1.11 1.66 2.25
    4.09 13400 53.57   9 26 65  1.11 1.66 2.25
    4.00 13922 54.38   6 26 68  1.26 1.68 2.26
    4.00 14163 55.32   5 24 70  1.26 1.68 2.26
    4.00 14117 55.14   6 24 70  1.26 1.68 2.26
    4.00 14101 55.14   6 24 70  1.26 1.68 2.26
    4.00 14742 57.59   3 23 74  1.26 1.68 2.26
    4.00 14088 55.08   6 24 70  1.32 1.68 2.26
    4.00 14259 55.71   5 24 71  1.32 1.68 2.26
    4.00 13565 52.99  10 25 64  1.32 1.68 2.26
    4.02 14033 55.11   7 24 70  1.32 1.68 2.26
    4.00 14003 54.70   6 25 69  1.32 1.68 2.26
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
    4.00 14045 54.86   6 24 70  1.30 1.67 2.25
    4.02 14180 55.64   5 23 72  1.30 1.67 2.25
    4.02 10075 39.53   7 26 67  1.30 1.67 2.25
    4.00 13942 54.52   7 24 69  1.30 1.67 2.25
    4.00 14366 56.12   5 24 72  1.30 1.67 2.25
    4.00 14189 55.43   5 24 71  1.27 1.66 2.24
    4.00 14033 54.82   6 24 70  1.27 1.66 2.24
    4.00 13795 53.89   9 24 67  1.27 1.66 2.24
    4.01 13869 54.28   5 23 72  1.27 1.66 2.24
    4.00 14295 55.84   5 23 72  1.27 1.66 2.24
    4.00 14090 55.05   6 24 70  1.25 1.65 2.23
    4.37 13560 57.86   5 27 67  1.25 1.65 2.23
    4.00 14304 55.87   6 23 71  1.25 1.65 2.23
    4.00 14192 55.44   7 23 70  1.25 1.65 2.23
    4.00 14129 55.19   6 23 70  1.25 1.65 2.23
    4.00 14521 56.72   3 24 73  1.23 1.64 2.23
    4.00 14651 57.23   3 23 73  1.23 1.64 2.23
    4.00 14608 57.06   3 24 73  1.23 1.64 2.23
    4.00 14311 55.95   3 24 73  1.23 1.64 2.23
    4.00 14149 55.27   6 24 70  1.23 1.64 2.23
              disk0       cpu    load average
    KB/t  tps  MB/s  us sy id   1m   5m   15m
    4.04 13180 51.98   5 24 70  1.21 1.63 2.22
    4.00 11314 44.20   5 24 70  1.21 1.63 2.22
    4.00 14513 56.69   4 23 74  1.21 1.63 2.22
    4.00 14278 55.77   6 24 71  1.21 1.63 2.22
    4.00 13690 53.54   7 24 69  1.21 1.63 2.22
    4.00 13817 54.01   6 26 68  1.59 1.70 2.24
    4.00 13449 52.53   8 25 67  1.59 1.70 2.24
    4.00 12436 48.59  12 27 62  1.59 1.70 2.24
    4.00 14305 55.88   4 24 72  1.59 1.70 2.24
    4.00 14090 55.04   4 26 70  1.59 1.70 2.24
    4.00 13668 53.39   7 25 67  1.55 1.69 2.23
    4.00 13279 51.87   9 26 65  1.55 1.69 2.23
    4.00 13972 54.64   4 24 71  1.55 1.69 2.23
    4.00 13638 53.27   7 26 67  1.55 1.69 2.23
    4.00 13297 51.94   9 25 66  1.55 1.69 2.23
    4.00 13142 51.34   9 26 65  1.58 1.69 2.23
    4.00 13979 54.61   5 25 70  1.58 1.69 2.23
    4.00 13631 53.25   7 26 67  1.58 1.69 2.23
    4.00 14355 56.07   4 23 73  1.58 1.69 2.23
    4.00 14486 56.65   3 23 74  1.58 1.69 2.23
```

Beacuse time is limited, I jsut used 1G bytes data. When turning on the O_SYNC flag, the writing speed is almost ten times slower.
For more details, you may refer to `fsync` posix api.


How does this happen?
=====================

From the docstring, we know that `os.write` is a c function implemented in CPython.
And the following code is implemented with posix api `write`.

```c
static Py\_ssize_t
_Py_write_impl(int fd, const void *buf, size_t count, int gil_held)
{
    Py_ssize_t n;
    int err;
    int async_err = 0;

    _Py_BEGIN_SUPPRESS_IPH
#ifdef MS_WINDOWS
    if (count > 32767 && isatty(fd)) {
        /* Issue #11395: the Windows console returns an error (12: not
           enough space error) on writing into stdout if stdout mode is
           binary and the length is greater than 66,000 bytes (or less,
           depending on heap usage). */
        count = 32767;
    }
    else if (count > INT_MAX)
        count = INT_MAX;
#else
    if (count > PY_SSIZE_T_MAX) {
        /* write() should truncate count to PY_SSIZE_T_MAX, but it's safer
         * to do it ourself to have a portable behaviour. */
        count = PY_SSIZE_T_MAX;
    }
#endif

    if (gil_held) {
        do {
            Py_BEGIN_ALLOW_THREADS
            errno = 0;
#ifdef MS_WINDOWS
            n = write(fd, buf, (int)count);
#else
            n = write(fd, buf, count);
#endif
            /* save/restore errno because PyErr_CheckSignals()
             * and PyErr_SetFromErrno() can modify it */
            err = errno;
            Py_END_ALLOW_THREADS
        } while (n < 0 && err == EINTR &&
                !(async_err = PyErr_CheckSignals()));
    }
    else {
        do {
            errno = 0;
#ifdef MS_WINDOWS
            n = write(fd, buf, (int)count);
#else
            n = write(fd, buf, count);
#endif
            err = errno;
        } while (n < 0 && err == EINTR);
    }
    _Py_END_SUPPRESS_IPH

    if (async_err) {
        /* write() was interrupted by a signal (failed with EINTR)
           and the Python signal handler raised an exception (if gil_held is
           nonzero). */
        errno = err;
        assert(errno == EINTR && (!gil_held || PyErr_Occurred()));
        return -1;
    }
    if (n < 0) {
        if (gil_held)
            PyErr_SetFromErrno(PyExc_OSError);
        errno = err;
        return -1;
    }

    return n;
}
```

This function is quite simple. Firstly, it checks the `count` size, then calls `write` api, finally checks whether error has occurred and return written count.

In python interpreter, pure c function is executed without native python stack frame overhead. Normally it can be executed faster than pure python function.
In this benchmark, the hottest operation is `os.write`, which runs as fast as c version `write`. Therefore the total time makes a little difference.

In conslusion, any program's writing speed is limited to the storage device. When the storage device is not saturated, the writing speed is direct proportion to program's execution speed.
Once the disk device is saturated, program can't write faster longer.


Reference
=========

  * open(2)

  * write(2)

  * fsync(2)

  * close(2)

  * iostat(1)

  * <https://en.wikipedia.org/wiki/POSIX>
