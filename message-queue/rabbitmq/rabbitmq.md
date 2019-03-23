
rabbitmq
========

rabbitmq是一个使用高级消息队列协议的开源消息代理软件，用Erlang编写而成。

rabbitmq的基本构成
==================

 * connection

 * channel

 * exchange

 * route

 * queue

 * virtual host


数据传输的基本模型
==================

生产者 --------> exchange ------> route_key ------> queue -------> 消费者


connection和channel的关系
=========================

在rabbitmq中，connection代表的是一个真实的TCP层的连接，而channel是在这个连接上分出来的一个虚拟通道，用来实现数据的传输。
Python代码示例如下,

```python
import pika

con1 = pika.BlockingConnection()
cha1 = con1.channel()
cha2 = con1.channel()
# do something with cha1 or cha2
```


四种类型的exchange
==================

 * fanout类型

此时用来路由的route_key是会被忽略的，因为不管是生产者还是消费都不需要使用它来进行消息的定向路由。
在此场景下，消息的传递相当与广播，只要与指定exchange绑定的queue都会收到生产者的消息。

 * direct类型

此时会通过route\_key来对应路由到具体的queue。exchange会根据生产者的route_key来进行选择queue。

 * topic类型

此时相当于对消息的路由进行定制，通过route\_key来进行模式的匹配。绑定到exchange的queue会指定一个pattern，
exchange收到生产者的消息时，会根据生产者指定的route_key来匹配与exchange绑定的queue的pattern,从而进行消息路由。

 * headers类型

与direct比较类似，但不同于direct的是route_key不仅仅只是字符串，而可能是整数或者hash结构的数据。匹配规则类似于direct。


queue
=====

queue作为一个中间媒介来存储生产者传输过来的消息，然后进行传输给消费者。


Message delivery gurantee
=========================

[Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/confirms.html#consumer-acks-multiple-parameter).


Reference
=========

  * <http://www.rabbitmq.com/tutorials/amqp-concepts.html>
