
Socket连接过程
==============

连接代码过程
------------


  * Client


```

import socket

c1 = socket.socket()

c1.connect(('', 80))

```

涉及socket(man 2)构造过程， 以及调用conenct(man 2)方法。


  * Server


```

import socket

s1 = socket.socket()

s1.bind(('', 80))

s1.listen()

c1, addr = s1.accept()


```

同样涉及到socket(man 2)构造过程，然后通过bind(man 2)绑定地址和端口，同时调用listen(man 2)来标志该socket可侦听，最后调用accept(man 2)来获取新建的连接。


状态迁移
--------

CLOSED  ------->  SYN_SENT (调用connect, 开始TCP三路握手，发送SYN字节流)   ---------->   收到ACK确认和SYN字节流    ---------> ESTABLISHED (发送ACK确认，connect成功返回)

                     |                                                                           ^
					 |                                                                           |
					 |                                                                           |
					 |                                                                           |
					 |                                                                           |
					 V                                                                           |

CLOSED ---------> LISTEN (调用listen，开始侦听)  --------> SYN_RECV (跟accept调用无关) -------->  发送带有ACK确认的SYN字节流  ------------> ESTABLISHED (收到ACK确认, 同时放入接收队列，等待accept取)



接收过程
============

accept过程
----------

调用accept时，从内核接收队列中获取已经建立好的连接，实际的连接由TCP协议栈内核实现；如果队列为空，accept可能会被阻塞(阻塞方式下), 直到队列中有新的连接。


队列限制
--------

接收队列满后，接收端会采取丢弃ACK确认包，重发SYN/ACK包让发起端重试，等待队列被消耗。重试次数见设置/proc/sys/net/ipv4/tcp\_synack_retries。详见<http://veithen.github.io/2014/01/01/how-tcp-backlog-works-in-linux.html>


connect错误说明
===============

  * ECONNREFUSED

试图连接的地址端口上并没有正在侦听的socket。

  * ETIMEDOUT

连接超时，可能在发起连接时进行/proc/sys/net/ipv4/tcp\_syn_retries次重试后依然没有三路握手成功，或者中间过程重传超时。


引用
====

  * man 2 socket

  * man 2 connect

  * man 2 bind

  * man 2 listen

  * man 2 accept

  * <http://veithen.github.io/2014/01/01/how-tcp-backlog-works-in-linux.html>
