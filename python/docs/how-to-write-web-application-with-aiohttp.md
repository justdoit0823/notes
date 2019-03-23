
aiohttp
=======

[aiohttp](https://github.com/aio-libs/aiohttp) is a http client and server framework based on [asyncio](https://docs.python.org/3/library/asyncio.html).

We can easily write the new coroutine style server programs with it. Meanwhile, there is a rich asynchronous http client for remote http requests, which is as easy as to another popular http client package [requests](https://github.com/requests/requests).

They both have the simple apis for developers, but works in much different ways. aiohttp is designed for asynchronous http request, which can be easily integrated into the asynchronous web server.


Features
--------

  * Supports both client and server side of HTTP protocol.

  * Supports both client and server Web-Sockets out-of-the-box.

  * Web-server has middlewares and pluggable routing.


Server
======

There are three important parts in the server program, `aiohttp.web.Application` object, router within the application object and route handler.

The application object receives external http request objects, routes to the correct handlers with request object, and returns corresponding responses.

Now, we can start to build a server program.


```python
from aiohttp import web


async def hello(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def echo(request):
	name = request.GET['name']
	message = await request.text()
	echo_msg = '{name} write message {msg}'.format(name=name, msg=message)
    return web.Response(text=echo_msg)


async def query_ipinfo(ip):
	with aiohttp.ClientSession() as session:
		url = 'http://ipinfo.io/{ip}'.format(ip)
		with session.get(url) as res:
			ret = await res.text()
			return ret


async def ip_query(request):
	ip = request.POST['ip']
	ret = await query_ipinfo(ip)
	return web.Response(text=ret)


def main():
	app = web.Application()
	app.router.add_get('/echo', echo)
	app.router.add_get('/hello/{name}', hello)
	app.router.add_post('/ip', ip_query)

	web.run_app(app)


if __name__ == '__main__':
	main()

```

A simple asynchronous http server is finished. We can simply run the server with `Python` command.

There are three steps for writing such a server.

  * write a http request handler, do your own business within this handler and return the result.

  * define a route with url pattern, http method and corresponding handler.

  * run the application.


Client
======

We can easily embed the client in server program, but how can we write idependent client programs?

```python
import asyncio
import sys

from aiohttp import web


async def query_ipinfo(ip):
	with aiohttp.ClientSession() as session:
		url = 'http://ipinfo.io/{ip}'.format(ip)
		with session.get(url) as res:
			ret = await res.text()
			return ret


def main():
	ip = ''
	if len(sys.argv) > 1:
		ip = sys.argv[1]

	loop = asyncio.get_event_loop()
	ret = loop.run_until_complete(query_ipinfo(ip))
	print(ret)


if __name__ == '__main__':
	main()

```

As above, client request is passively triggered in server programs. But in client programs we need to start the request actively.

With the event loop provided by asyncio, we can call `run_until_complete` function to execute coroutine object one by one.

Now things are clear, we write independent request coroutine functions and have them exeuted by the event loop.


Compared to tornado
====================

[tornado](http://www.tornadoweb.org/en/stable/index.html) is also an asynchronous web server framework, but different from aiohttp.

  * coroutine

aiohttp uses Python's native coroutine while tornado uses the coroutine simulated with generator. They are used to implement the same function, but work in different ways.

  * http client

tornado only provides a very simple asynchronous http client, so users have to take more attention to the relevant http details when doing http request.

With aiohttp, we can easily use the apis without any other care.

  * performance

aiohttp has better performance than tornado, and we can get the details of the benchmark at [py-frameworks-bench](http://klen.github.io/py-frameworks-bench/).

I believe the native coroutine acts as an important factor here.


Reference
=========

  * <https://github.com/aio-libs/aiohttp>

  * <http://aiohttp.readthedocs.io/>
