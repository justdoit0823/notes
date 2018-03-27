

HTTP2
=====

HTTP/2 is a replacement for how HTTP is expressed “on the wire.” It is not a ground-up rewrite of the protocol; HTTP methods, status codes and semantics are the same, and it should be possible to use the same APIs as HTTP/1.x (possibly with some small additions) to represent the protocol.

The focus of the protocol is on performance; specifically, end-user perceived latency, network and server resource usage. One major goal is to allow the use of a single connection from browsers to a Web site.


Specification
-------------

  * HTTP2

[Hypertext Transfer Protocol version 2](http://httpwg.org/specs/rfc7540.html).


  * HPACK

[Header Compression for HTTP/2](https://httpwg.github.io/specs/rfc7541.html).


Implementation
----------------

### Client ###

  * hyper

  * h2load


### Server ###

  * gRPC

  * envoy

  * nghttp2


Read more detail at [implementations](https://github.com/http2/http2-spec/wiki/Implementations).


gRPC
----

gRPC is a RPC framework developed at google, which deliveries messages with HTTP2.


### protocol ###

Go to [protocol-http2](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md).


FAQ
---

Go to [faq](https://http2.github.io/faq/).


Reference
=========

  * <https://http2.github.io/>
