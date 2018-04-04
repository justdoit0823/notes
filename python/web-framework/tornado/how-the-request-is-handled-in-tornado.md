
From request to response in tornado
====================================

Related objects
----------------

  * application

`tornado.web.Application`.

  * http server

`tornado.httpserver import HTTPServer`.

  * request stream

`tornado.iostream.IOStream`.

  * server connection

`tornado.http1connection.HTTP1ServerConnection`.

  * request connection

`tornado.http1connection.HTTP1Connection`.

  * request object

`tornado.httputil.HTTPServerRequest`.

  * request handler

`tornado.web.RequestHandler`.


Server
------

  * initialize http server

`web.Application` as the `request_callback` argument.

  * bind http server

  * start http server


Incoming request
----------------

### Handle connection ###

  * initialize IOStream with accepted connection


### Handle stream ###

  * initialize HTTP1ServerConnection

  * start serving of HTTP1ServerConnection(httpserver as the delegate param)


### Handle HTTP1 server connection ###

  * start server-request loop

  * initialize HTTP1Connection

  * start request in the httpserver


### HTTPServer start request ###

  * application start request

  * call method start_request of application's router

  * return request delegate


### Handle HTTP1 connection ###

  * read request message

  * read header

  * parse header(delegate to the router)

  * read body

  * finish request delegation(routing delegate)


### Routing delegate ###

  * receive header

  * initialize HTTPServerRequest

  * find handler

  * delegate to request handler


### Handler delegate ###

  * receive header

  * receive data

  * execute handler(after finishing delegation if the request hasn't stream body)


### RequestHandler execution ###

  * execute

  * call request's method


Outgoing response
-----------------

### Write response ###

  * write response


### Finish request ###

  * finish RequestHandler

  * finish HTTPServerRequest

  * finish HTTP1Connection
