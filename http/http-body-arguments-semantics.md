
HTTP
====

超文本传输协议（HTTP）是一个共享的，协作的和超媒体信息系统的应用层协议。从1990年开始被万维网上的信息使用。

HTTP/0.9是第一个通过网路传输原始数据的简单协议版本。在[RFC 1945][RFC 1945]中定义的1.0版本对协议做了一些改进，

允许类似MIME格式的消息，传输的数据中包含一些原始信息可以对请求和响应的语义做一些改变。

然而，1.0版本并没有充分考虑到分层代理，缓存，长连接，和虚拟host。

另外，自称HTTP/1.0的应用不断传播，然而并没有完全实现HTTP/1.0协议；这迫使HTTP版本需要改变，

以支持两个互相通信的应用能确定对象支持的版本。


[RFC 1945]: https://tools.ietf.org/html/rfc1945


URI
===


更进一步，URI可以被分成定位部分(URL)，名称部分(URN)或者两者。

术语“URL”表示在URI中通过主要的访问路径来确定资源的一部分（如网路地址），而不是通过名字或者资源的其它属性。

术语“URN”表示在URI中保持全局唯一和在资源不存在或不可用情况下持久定位必须的一部分。



HTTP Methods
============

  * GET


		访问的资源被URI定位，body参数不符合语义。


  * HEAD


		除了响应中不包括消息body外，跟GET是一样的。同样，body参数不符合语义。


  * POST


		资源被URI定位，提交的body数据追加到资源中。


  * PUT


		资源被URI定位，资源不存在时，提交的body数据用来创建一个用URI标识的资源；

		资源存在时，提交的body数据用来更新资源。


  * DELETE


		资源被URI定位，并删除资源或移动到不可访问的位置。body参数不符合语义。


  * OPTIONS


		资源被URI定位，body参数没有实际用处，保留做扩展。


请求参数总结
============


| Method | Query | Body |
| ------- | ------ | ------ |
| GET  | 不必须 | 不应该 |
| POST | 不必须 | 必须 |
| PUT  | 不必须 | 必须 |
| DELETE | 不必须 | 不应该 |
| OPTIONS | 不必须 | 暂时无意义 |



引用
====


  * <https://tools.ietf.org/html/rfc2616#section-9.3>


  * <https://tools.ietf.org/html/rfc2396>


  * <http://stackoverflow.com/questions/978061/http-get-with-request-body>
