
故事的由来
==========

这是一个发生在生产环境的真实案例，发现蹊跷之后想了很长时间，也查了很多地方。由于不能完全复现现场，然后只能靠着仅有的一处报错日志和代码逻辑进行盘查。

在复盘的过程中对TCP层的一些网络参数有了更深刻的认识和理解，以及对TCP层传输时可能发生的状况有了更全面的了解并且掌握了更利于排查的工具和思路。


一个不正常的502报警邮件
=======================

在愚人节上午11点多时，收到了一封报警邮件，一看里面有我维护的接口出现502了。虽然nginx层配置了proxy\_next\_upstream_tries，不会影响端上的接口，但还是谨慎地上线查看了一下，发现进程没挂也没有被重启，进程状态(S)也是正常的。

如是就用netstat查看了一下进程的连接情况，发现了一些细节，可以解释502产生的原因了。

假死进程中的未读数据
--------------------

netstat的结果显示，有好几个连接都有未读取的数据，具体表现中输出中Recv-Q列中的数据项不是0，其中既有Tornado的监听连接，也有其它的正常连接。

其中，监听连接的SYN连接积压值为129，已经超过了监听队列能够hold住的数量，所以才导致新的请求连接在发送数据时被拒，上层表现就是nginx 502。那么为什么会积压这么多没有被接受的连接呢？只有一个解释，进程阻塞了，导致不能及时处理这些新进来的请求。

**至此，可以得到第一个结论，进程没有挂而是阻塞住了，监听队列被充满了。**


队列长度为什么是129
-------------------

这里的队列长度是监听套接字在listen时指定的，内核2.2之后表示完成3路握手正常建立连接的总数，区别于以前包含已建立连接和未完成连接。同时Tornado框架里面监听时默认值就是128，这就出现了上面的场景。

顺便查看了一下kernel的代码，发现判断是否overflow是从0开始，所以netstat的输出中会是129.


超过监听队列长度会怎么样
------------------------

当连接已建立（完成三次握手）的数目超过listen时指定的数目时，server端收到新到的SYN分节时会同正常三路握手一样发送SYN-ACK分节（正常进入SYN_RECV状态）；但是，在收到后续的数据时，server端TCP会开启一个特殊的定时器用来发送SYN-ACK分节，发送的次数可以通过net.ipv4.tcp\_synack\_retries设置。通过丢弃ACK，让客户端TCP可以重新发送ACK确认，使连接请求尽可能被接受。

超过SYN-ACK重试次数之后，该套接字会被关闭不可用，若是有数据分节（包括只有ACK的分节）发送过来，server端TCP层会重置连接。另外，根据listen(man 2)手册上面的说明，开启syncookies时，逻辑上不存在最大数量的限制；在关闭syncookies时，超过net.ipv4.tcp\_max\_syn_backlog时，新收到的SYN分节会被丢弃掉，让客户端重传，超过重传次数之后引发ETIMEDOUT。

这就解释了上面nginx 502产生的原因了，建立连接时不会直接报错，但是发送数据的时候引发对端重置连接。这种502的情况跟进程挂掉的表现虽然在nginx层面是一样的，但是背后的出错原因却是不同的。


连接如何失败
------------

  * ETIMEDOUT

在阻塞情况下，套接字尝试发起连接请求时可能发生的错误，有可能是丢包且超过重传次数时报错的；也有可能是上面那种server端“太忙”导致的。

  * ECONNREFUSED

套接字尝试发起连接请求时可能发生的错误，由于server端并没有监听连接，收到client端发过来端SYN分节时，TCP会直接发送RST分节，重置连接。


可能阻塞的地方
===============

Traceback的定位
---------------

根据traceback的定位，在一处查询操作时sqlalchemy报错了，但是该方法被装饰器包装了，会先去读取缓存。所以执行的顺序是，先去Redis查询看能否命中缓存，然后才是去查询MySQL。

连接Redis
---------

看了一眼连接Redis server的package，发起连接的时候使用阻塞方式，也就是确实存在阻塞的可能性。另外，默认不开启连接timeout，读写timeout，以及TCP层keepalive。一旦阻塞了，在client端不会进行任何探测以及超时报错。

连接RDS
-------

用sqlalchemy进行数据库操作时，连接也是使用阻塞方式，但默认开启TCP层keepalive，同时在发起连接时可以指定连接timeout，但是并没有看到任何地方支持设置读写timeout。所以，也可能发生阻塞，client会进行探测，不会一直阻塞住，这一点跟连接Redis的时候不同。


排查问题
========

报错的地方
----------

出错日志显示是在进行MySQL查询的时候，应用层报错“Lost connection to MySQL server during query”。所以，连接出错的地方是在进行SQL查询，而且未成功返回结果，但是这并不能直接断定阻塞的地方就是这里。

阻塞的时间
----------

7881849.28ms = 2 \* 3600 \* 1000ms + 75 \* 9 \* 1000ms + 6849.28ms

排查Redis
---------

虽然redis client是可能阻塞的，但是由于没有任何超时和探测机制，如果阻塞了，client自己是不会有机会报错的。那么看看Redis server会不会释放连接或者发送数据，结束client端阻塞。

实际上，Redis server既支持keepalive探测，也支持应用层timeout。在配置文件中有明确说明，如下：

```
# Close the connection after a client is idle for N seconds (0 to disable)
timeout 0

# TCP keepalive.
#
# If non-zero, use SO_KEEPALIVE to send TCP ACKs to clients in absence
# of communication. This is useful for two reasons:
#
# 1) Detect dead peers.
# 2) Take the connection alive from the point of view of network
#    equipment in the middle.
#
# On Linux, the specified value (in seconds) is the period used to send ACKs.
# Note that to close the connection the double of the time is needed.
# On other kernels the period depends on the kernel configuration.
#
# A reasonable value for this option is 300 seconds, which is the new
# Redis default starting with Redis 3.2.1.
tcp-keepalive 300
```

然而，一看Redis的配置，timeout是10个小时，没有开启TCP层keepalive。因此，可以肯定在上面的阻塞时间段内server端肯定不会释放连接的。

那么，server可能在2小时之后发送响应数据吗？几乎没有可能，首先超时重传没有这么长的时间，网络拥塞的可能性也很小；在这次案例中更是不可能，后面会说到。

断定RDS
-------

sqlalchemy连接MySQL时使用的是进程级的连接池，同时连接的回收时间设置成1小时，如果真是阻塞在连接Redis那里，那么接下来的SQL查询会重新建立连接，从事实来看要么是重用连接（未超过1小时），或者重新成功建立连接。不管哪种情况，此时网络正常，都不太可能在接下来都短时间内报错。

另外，MySQL server设置的net\_read\_timeout和net\_write\_timeout分布是30秒和1分钟，而且主键查询也不太可能引发这两种情况；另外设置的wait_timeout变量的值是24小时，所以也不太可能是MySQL server的超时机制。

首先，可以肯定的是sqlalchemy发送查询请求成功了，不然读取查询响应不会阻塞这么长时间，至于有没有重传很难说。那么MySQL server肯定收到请求数据了，而且没有看到慢查询，比较大的可能是响应的数据流丢失了而且超时重传失败了，导致sqlalchemy端收不到数据一直阻塞。

至此，基本上可以肯定是由于TCP层keepalive机制，导致连接被重置继而报错，把线程从挂起状态给捞了回来；而且是sqlalchemy端的探测导致收到连接被重置的RST分节，然后报错。因为sqlalchemy端没有任何会主动重置连接的操作了，MySQL server端由于超时已经关闭该套接字了，收到探测分节之后发送RST重置连接，这跟MySQL的错误码也是吻合的。

由于MySQL server端超时重传消耗了几十分钟，那么总的时间应该比上面的总时间长？不竟然，因为keepalive的定时器是建立完连接之后根据SO_KEEPALIVE标志来决定是否开启，所以在上面的总时间窗口是成立的。


场景回放
--------

在进行数据库查询操作时，client首先发送查询数据流，返回成功，实际数据并没有成功发送到对端TCP，之后就阻塞在读取查询响应上。MySQL server收到请求后进行处理，并且发送返回的结果数据流，但是由于网络问题重传无果，导致client并没有收到数据，一直hang住。

由于client开启了keepalive探测，定时器超时后发起探测，这时网络状况正常，MySQL server收到了client端发过来的探测分节，直接重置连接，导致client读操作报错，结束了一段等待。

TCP层细节
----------

  * send返回成功

程序通过套接字send数据成功，只能表示数据成功复制到套接字的发送缓冲区了，并不表示数据发送成功，也不表示对端TCP已经收到。然后沿着协议栈向下传递了，等着TCP根据各种既定策略来发送。

注意，这跟TCP是可靠的传输协议并不冲突，这里的可靠不是不丢数据，而是在丢数据发生时尽可能重传，保证数据有序到达，不错乱，丢弃重复的数据。对于实际上对端有没有收到数据，需要应用层自己确认。

  * 超时重传

在TCP发送出数据后，若不能收到确认，TCP会根据重传策略进行多次尝试，具体次数可以通过net.ipv4.tcp\_retries1（要求网络层更新路由阀值）和net.ipv4.tcp_retries2（最大重试次数）设置，一般大约13到30分钟。

超过最大重传次数之后，套接字状态变成CLOSE状态，进入不可用状态；错误码字段会被写入具体的错误码，后续的读写操作都会报相应的错误（设置错误之前开始的读操作可能会返回一部分数据），同时相应的定时器也会被清除。对于对端TCP发送过来的任何数据，都会发送RST分节重置连接。

我是这样理解的，如果允许后续的写操作，为了保证数据有序，那么还要重传之前丢失的数据，而之前重传了几十分钟都不行，还不如放弃重新建立连接，简化逻辑过程。


  * keepalive

TCP keepalive是TCP实现中一个可选的功能，用来探测对端连接是否存在。通过SO\_KEEPALIVE，TCP\_KEEPIDLE，TCP\_KEEPCNT, TCP\_KEEPINTVL可对每个套接字进行设置，同时也可通过net.ipv4.tcp\_keepalive\_time, net.ipv4.tcp\_keepalive\_probes, net.ipv4.tcp\_keepalive_intvl来进行系统级的设置。

其中，TCP\_KEEPIDLE是指定探测的周期，TCP\_KEEPINTVL是指定发送探测分节的间隔，TCP_KEEPCNT是指定发送探测分节的最大次数；可以动态设置，立即生效；但是收到对端发送过来的数据时，不会重置探测时间，也就是只跟对这四个参数的设置有关。连接建立成功后，开启keepalive就会启动定时器。

超过最大探测次数后，套接字状态会变成CLOSE状态，进入不可用状态，类似于超时重传。


  * TCP层

TCP层相当于运行在内核态的一个发送和接收代理，应用进程通过系统调用来与协议栈交互来发送和接收数据，有些操作能实时得到实际结果，但是有些操作并不能实时能得到实际结果，只要代理按规矩办事就行。

就拿发送数据来说，调用时相当于进程给代理交代了一件事情，但又不会死等代理的结果，去干别的事了；代理收到任务之后也不是马上就干这一件事，而是根据直接的安排考虑一下该如何做最合理；各自就继续happy去了。

接收数据时，代理收到一堆结果，但并不是来一个结果就立马告诉进程，而是先给整理好，等进程来要的时候一块儿给；如果发生了什么意外呢，代理也是自己先硬扛着，等进程来问的时候老实交代就行。


如何处理阻塞套接字
==================

在用阻塞套接字进行读操作的时候，由于网络状况的不确定性因素，可能导致线程被挂起，一直hang住，影响单线程程序的正常运行。那么，我们该如何去避免呢？首先，系统层提供了给套接字设置发送和读取超时时间的选项，另外就是应用层自己做封装，把单个阻塞操作转移到带超时机制的系统调用上来，靠事件来驱动。


系统层套接字选项
----------------

系统提供了两个套接字层的选项SO\_RCVTIMEO和SO_SNDTIMEO，分别用来设置读取和发送的超时时间，避免长时间阻塞。在超时之前，如果已经发送或者读取完指定长度的数据，那么正常返回；超时之后，如果已经发送或者读取了一部分数据，那么返回已发送或读取数据的长度，否则就是返回-1，错误码会设置成EAGAIN等。

另外，经测试macOS上面connect操作不支持此选项。


应用层封装（Python中如何解决这些问题）
----------------------------------

Python中封装的socket对象提供了设置timeout功能，在做任何可能阻塞操作之前，可以设置超时时间，这样就不会长时间阻塞线程的运行了。或者，对套接字操作时，可以设置为非阻塞模式，这样不能立即完成的操作都会马上返回错误，不会阻塞线程。另外，也可以通过setsockopt方法来给套接字设定TCP的三个keepalive参数（macOS下不支持设置TCP_KEEPIDLE），进而控制套接字的keepalive行为。

连接redis的package里面就是对此进行来封装，提供了超时和keepalive机制。

### Python中如何设置超时 ###

在Python中做套接字操作时，通过调用socket.settimeout方法时指定超时时间，接下来的操作如建立连接和读写数据就会按此生效。针对参数有三种解释，值为None时，设置套接字为阻塞模式；值为0时，仅设置套接字为非阻塞模式；值为非0正数时，设置套接字为非阻塞模式，同时设置超时为value秒；更加详细的请移步官网文档<https://docs.python.org/3/library/socket.html#socket-timeouts>。

### Python如何实现给套接字设置超时 ###

原理其实很简单，就是把套接字在单个阻塞操作中转移到带超时机制的阻塞调用上，如select，poll，epoll等。在进行poll操作前，把套接字的使用模式设置为非阻塞（跟通过poll获取事件无关），然后发生事件发生后poll操作返回，再进行具体的套接字操作（设置非阻塞的真是目的，防止事件发生后操作依然可能阻塞，如多进程监听一个端口）。

具体实现套接字操作代码细节如下：

```
/* Call a socket function.

   On error, raise an exception and return -1 if err is set, or fill err and
   return -1 otherwise. If a signal was received and the signal handler raised
   an exception, return -1, and set err to -1 if err is set.

   On success, return 0, and set err to 0 if err is set.

   If the socket has a timeout, wait until the socket is ready before calling
   the function: wait until the socket is writable if writing is nonzero, wait
   until the socket received data otherwise.

   If the socket function is interrupted by a signal (failed with EINTR): retry
   the function, except if the signal handler raised an exception (PEP 475).

   When the function is retried, recompute the timeout using a monotonic clock.

   sock_call_ex() must be called with the GIL held. The socket function is
   called with the GIL released. */
static int
sock_call_ex(PySocketSockObject *s,
             int writing,
             int (*sock_func) (PySocketSockObject *s, void *data),
             void *data,
             int connect,
             int *err,
             _PyTime_t timeout)
{
    int has_timeout = (timeout > 0);
    _PyTime_t deadline = 0;
    int deadline_initialized = 0;
    int res;

#ifdef WITH_THREAD
    /* sock_call() must be called with the GIL held. */
    assert(PyGILState_Check());
#endif

    /* outer loop to retry select() when select() is interrupted by a signal
       or to retry select()+sock_func() on false positive (see above) */
    while (1) {
        /* For connect(), poll even for blocking socket. The connection
           runs asynchronously. */
        if (has_timeout || connect) {
            if (has_timeout) {
                _PyTime_t interval;

                if (deadline_initialized) {
                    /* recompute the timeout */
                    interval = deadline - _PyTime_GetMonotonicClock();
                }
                else {
                    deadline_initialized = 1;
                    deadline = _PyTime_GetMonotonicClock() + timeout;
                    interval = timeout;
                }

                if (interval >= 0)
                    res = internal_select(s, writing, interval, connect);
                else
                    res = 1;
            }
            else {
                res = internal_select(s, writing, timeout, connect);
            }

            if (res == -1) {
                if (err)
                    *err = GET_SOCK_ERROR;

                if (CHECK_ERRNO(EINTR)) {
                    /* select() was interrupted by a signal */
                    if (PyErr_CheckSignals()) {
                        if (err)
                            *err = -1;
                        return -1;
                    }

                    /* retry select() */
                    continue;
                }

                /* select() failed */
                s->errorhandler();
                return -1;
            }

            if (res == 1) {
                if (err)
                    *err = SOCK_TIMEOUT_ERR;
                else
                    PyErr_SetString(socket_timeout, "timed out");
                return -1;
            }

            /* the socket is ready */
        }

        /* inner loop to retry sock_func() when sock_func() is interrupted
           by a signal */
        while (1) {
            Py_BEGIN_ALLOW_THREADS
            res = sock_func(s, data);
            Py_END_ALLOW_THREADS

            if (res) {
                /* sock_func() succeeded */
                if (err)
                    *err = 0;
                return 0;
            }

            if (err)
                *err = GET_SOCK_ERROR;

            if (!CHECK_ERRNO(EINTR))
                break;

            /* sock_func() was interrupted by a signal */
            if (PyErr_CheckSignals()) {
                if (err)
                    *err = -1;
                return -1;
            }

            /* retry sock_func() */
        }

        if (s->sock_timeout > 0
            && (CHECK_ERRNO(EWOULDBLOCK) || CHECK_ERRNO(EAGAIN))) {
            /* False positive: sock_func() failed with EWOULDBLOCK or EAGAIN.

               For example, select() could indicate a socket is ready for
               reading, but the data then discarded by the OS because of a
               wrong checksum.

               Loop on select() to recheck for socket readyness. */
            continue;
        }

        /* sock_func() failed */
        if (!err)
            s->errorhandler();
        /* else: err was already set before */
        return -1;
    }
}
```


应用程序的设计
==============

在应用程序中一般都要做一些网络操作，有些操作又能挂起线程，导致线程无法继续执行；而且很多网络状况都是不可测的，环境复杂，需要应用自己给自己续命。

全部阻塞模式
------------

这个应该是很多web应用程序的运行方式，选择阻塞模式，保持清晰的执行顺序，然后用容器程序来跑web程序。这样在面对这种网络短暂问题导致可能发生的线程阻塞问题是如何应对的呢？只要连接都给设置上超时，又或者定时重启，根据处理过的请求数重启，简单粗暴。


全部非阻塞模式
--------------

这是一种很好地避免阻塞的方式，虽然偶有执行顺序各种乱跳，但是不会受困于网络，靠事件驱动，不会出现一些乱七八糟的情况。


阻塞非阻塞混合模式
-----------------

全部非阻塞听上去很美好，但现实情况下很难, 很多依赖的package都是阻塞调用的方式。理想很丰满，现实很骨感。另外，框架都有自己封装的事件循环（如Tornado有自己，Python3也有自带的），package很难用一种统一的方式去搞，只能搞适配，进一步增加了去阻塞化的难度。


工具
====

构建实验环境的第一步就是装好ipython，然后多开几个tab。部分不需要交互的实验步骤，可以通过脚本运行，更有节奏。


netstat
-------

带上-o选项，就能看到连接的各种定时器了，包括keepalive的，retransmission的和off情况的。具体解释可以看<https://superuser.com/questions/240456/how-to-interpret-the-output-of-netstat-o-netstat-timers>。另外，升级版是ss。

iptables
--------

用来模拟丢包情况，然后通过tcpdump查看具体网络过程。


后记
====

由着自己的好奇心，想了好几天这事，前前后后捋这个过程，判断和排查可能出错的地方；然后通过查看手册，做实验尝试观察输出结果，加上阅读实际内核代码，整理出来这些东西。遇着不确定的地方，都去反复思考和验证，硬逼着自己去了解更多的东西，把TCP层的一部分东西给捋清楚。

同时，每个节点又连着其它的，不可能一口气把所有的都完完全全明白之后再来个大总结，所以先根据现象结果整理记录这么多。另外，感慨一句，写100%能工作的代码跟写80%能工作的绝不是概率上的那20%。


引用
====

  * <http://veithen.github.io/2014/01/01/how-tcp-backlog-works-in-linux.html>

  * <https://en.wikipedia.org/wiki/Keepalive>

  * <https://docs.python.org/3/library/socket.html#socket-timeouts>

  * <https://superuser.com/questions/240456/how-to-interpret-the-output-of-netstat-o-netstat-timers>

  * man 7 tcp

  * man 7 socket

  * man netstat

  * man 2 listen

  * man iptables

  * man tcpdump
