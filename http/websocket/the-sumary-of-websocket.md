
WebSocket
=========

A WebSocket server is a TCP application listening on any port of a server that follows a specific protocol, simple as that.

The task of creating a custom server tends to scare people; however, it can be easy to implement a simple WebSocket server on your platform of choice.


Handshake
=========

First of all, the server must listen for incoming socket connections using a standard TCP socket.

Depending on your platform, this may be handled for you already.

For an example, let's assume that your server is listening on example.com, port 8000, and your socket server responds to GET requests on /chat.


Client Handshake Request
------------------------

```
GET /chat HTTP/1.1
Host: example.com:8000
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Connection header field must be Upgrade, and Upgrade header field must be websocket.

Common headers like User-Agent, Referer, Cookie, or Authentication headers might be there.

If any header is not understood or has an incorrect value , the server should send a "400 Bad Request" and immediately close the socket.

If the server doesn't understand that version of WebSockets, it should send a Sec-WebSocket-Version header back that contains the version(s) it does understand.

**Tip: All browsers will send an Origin header, server can use this for permission check.**


Server Handshake Response
-------------------------

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

After sending response, the handshake is finished. The server can send other headers like Set-Cookie, or ask for authentication or redirects via other status codes, before sending the reply handshake.


**Note: The server need to keep track of client websocket connections.**


Exchange Data Frames
====================

Format
------

```
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
| |1|2|3|       |K|             |                               |
+-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
|     Extended payload length continued, if payload len == 127  |
+ - - - - - - - - - - - - - - - +-------------------------------+
|                               |Masking-key, if MASK set to 1  |
+-------------------------------+-------------------------------+
| Masking-key (continued)       |          Payload Data         |
+-------------------------------- - - - - - - - - - - - - - - - +
:                     Payload Data continued ...                :
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
|                     Payload Data continued ...                |
+---------------------------------------------------------------+
```

Payload Length
--------------

Read bits 9-15 (inclusive) and interpret that as an unsigned integer.

  * Above result is 125 or less

That's the payload length.


  * Above result is 126

Read the next 16 bits and interpret those as an unsigned integer. 


  * Above result is 127

Read the next 64 bits and interpret those as an unsigned integer.

```
def payload_length(payload):

	__, payloadlen = struct.unpack("BB", payload[:2])
	payloadlen &= 0x7f
	if payload <= 125:
		return payloadlen
	elif payload == 126:
		return struct.unpack("!H", data[2: 4])[0]
	elif payload == 127:
		return struct.unpack("!Q", data[2: 10])[0]
```

Message Fragmentation
---------------------

The FIN and opcode fields work together to send a message split up into separate frames.

This is called message fragmentation. Fragmentation is only available on opcodes 0x0 to 0x2.

If it's 0x1, the payload is text. If it's 0x2, the payload is binary data. However, if it's 0x0, the frame is a continuation frame. 


WebSocket Heartbeat
===================


At any point after the handshake, either the client or the server can choose to send a ping to the other party.

When the ping is received, the recipient must send back a pong as soon as possible. You can use this to make sure that the client is still connected, for example.

A ping or pong is just a regular frame, but it's a control frame.

Pings have an opcode of 0x9, and pongs have an opcode of 0xA. When you get a ping, send back a pong with the exact same Payload Data as the ping (for pings and pongs, the max payload length is 125). You might also get a pong without ever sending a ping; ignore this if it happens.


Close Connection
================

To close a connection either the client or server can send a control frame with data containing a specified control sequence to begin the closing handshake (detailed in Section 5.5.1).

Upon receiving such a frame, the other peer sends a Close frame in response. The first peer then closes the connection. Any further data received after closing of connection is then discarded. 


How To Authenticate
===================

HTTP Basic Authenticate
-----------------------

First begin a full http basic authentication, and then start connecting to websocket server.


HTTP Cookie
------------

When client starts a websocket connection, the cookie header can be included. So the client need to authenticate with a http request before.


Ticket
--------

Get an authentication ticket from a regular authentication system, then send as query param to server.


Reference
=========

  * <https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers>

  * <https://zh.wikipedia.org/wiki/WebSocket>

  * <https://devcenter.heroku.com/articles/websocket-security#authentication-authorization>

  * <https://tools.ietf.org/html/rfc6455#section-4>
