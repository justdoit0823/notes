
IOLoop
======

Now there are more and more frameworks or packages which supports event ioloop interface for asynchronous programing, such as `tornado`, `asyncio`, `aiohttp`.
Though they support ioloop interface, the implementation is different from each others.

Let's take some examples.


Programming in tornado
-----------------------

```python
import functools

from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

@coroutine
def fetch_url(url):
	res = yield AsyncHTTPClient().fetch(url)
	return res.body


io_loop = IOLoop.instance()
io_loop.run_sync(functools.partial(fetch_url, 'https://jsonplaceholder.typicode.com/posts/1'))
```

Here, I define a coroutine function `fetch_url`, which retrieves a url and returns a response object.
And I initialize an ioloop object `io_loop`, synchronously execute coroutine function `fetch_url`.
The output may be printed as the foloowing:

```
b'{\n  "userId": 1,\n  "id": 1,\n  "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",\n  "body": "quia et suscipit\\nsuscipit recusandae consequuntur expedita et cum\\nreprehenderit molestiae ut ut quas totam\\nnostrum rerum est autem sunt rem eveniet architecto"\n}'
```

We have gotten the http response from url `https://jsonplaceholder.typicode.com/posts/1`.


Programming in aiohttp
----------------------

```python
import asyncio

import aiohttp

async def fetch_url(url):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as res:
			ret = await res.text()
			return ret


io_loop = asyncio.get_event_loop()
io_loop.run_until_complete(fetch_url('https://jsonplaceholder.typicode.com/posts/1'))
```

Likewise, we got the same http response in Python 3 native asynchronous way.


IOLoop in multithreading program
==================================

Sometimes we may use ioloop objects in a multithreading python program. How do we correctly use the ioloop object in this situation?
We discuss the different implementations between `tornado` and `asyncio` separately.


In tornado multithreading program
---------------------------------

### How to construct an ioloop object ###

There are two ways to initialize an ioloop objetc.

  * directly construct a IOLoop object

```python
from tornado.ioloop import IOLoop

io_loop = IOLoop()
```

>By default, a newly-constructed `IOLoop` becomes the thread's current
>`IOLoop`, unless there already is a current `IOLoop`. This behavior
>can be controlled with the ``make_current`` argument to the `IOLoop`
>constructor: if ``make_current=True``, the new `IOLoop` will always
>try to become current and it raises an error if there is already a
>current instance. If ``make_current=False``, the new `IOLoop` will
>not try to become current.

From the documentation, the first constructed `IOLoop` object will become the current ioloop object in the calling thread.
The following construction will also return the ioloop object, but won't become the current ioloop object unless `True` is passed to argument `make_current`.

So, we can safely initialize an ioloop object in this way within a multithreading python program.


  * call function `IOLoop.instance`

```python
from tornado.ioloop import IOLoop

io_loop = IOLoop.instance()
```

>Most applications have a single, global `IOLoop` running on the
>main thread.  Use this method to get this instance from
>another thread.  In most other cases, it is better to use `current()`
>to get the current thread's `IOLoop`.

From the documentation, the function `IOLoop.instance` returns a global ioloop object whenever is called.
Whether in the main thread or other threads, the return value is the same.

So, we can't initialize thread's private ioloop object with this function. The threads which has called this function share the same ioloop object.
However it's useful to retrieve the shared ioloop object between the whole threads.

Therefore, the best practice is constructing an ioloop object with the function `IOLoop.instance` within the main thread and directly constructing an ioloop object within the other threads.


### How to retrieve ioloop object ###

The tornado ioloop class `IOLoop` supports a function `current` for retrieving thread's current ioloop object.
Normally this function returns the thread's current ioloop object, but calls the function `IOLoop.instance` and returns the global ioloop object.
When the calling thread hasn't ioloop object, there may be a pitfall, however it returns the global ioloop object.
Fortunately, we can pass `False` to the argument `instance` to avoid this situation.


In asyncio multithreading program
---------------------------------

### How to construct an ioloop object ###

```python
import asyncio

io_loop = asyncio.new_event_loop()
asyncio.set_event_loop(io_loop)
```

In `asyncio` package, the default event loop policy interface supports a function `new_event_loop` to construct an ioloop object.
We can create new ioloop object with this function in any threads, but we should explictily call function `set_event_loop` if there’s need to set the ioloop as the current thread's ioloop object.


### How to retrieve ioloop object ###

```python
import asyncio

io_loop = asyncio.get_event_loop()
```

The default event loop policy interface also supports a function `get_event_loop` to retrieve current thread's ioloop object.
When it's called within the main thread, it returns an ioloop object despite whether there is already an ioloop object.
However, the interpreter will raise `RuntimeError` when current thread is not the main thread and hasn't an ioloop object yet.
So, we need to create an ioloop object before retrieving in the other threads.


But, you can customize the event loop policy to behave as what you think. See more details at [customizing-the-event-loop-policy](https://docs.python.org/3/library/asyncio-eventloops.html#customizing-the-event-loop-policy).


Test program
============

```python
import asyncio
import threading

from tornado.ioloop import IOLoop

def non_main_thread_task(t_io_loop):
	assert IOLoop.current(False) is None, "invalid current thread's ioloop object."
	assert IOLoop.current() is t_io_loop, ""

	io_loop = IOLoop()
	assert t_io_loop is not io_loop, "invalid new ioloop object."
	assert IOLoop.current() is io_loop, "IOLoop.current returns invalid ioloop object."

	try:
		a_io_loop = asyncio.get_event_loop()
	except RuntimeError:
		pass
	else:
		assert False, "invalid current's asyncio ioloop object."

	a_io_loop = asyncio.new_event_loop()

	try:
		a_io_loop = asyncio.get_event_loop()
	except RuntimeError:
		pass
	else:
		assert False, "invalid current's asyncio ioloop object."

	asyncio.set_event_loop(a_io_loop)
	try:
		ag_io_loop = asyncio.get_event_loop()
	except RuntimeError:
		assert False, "get_event_loop returns invalid ioloop object."
	else:
		assert a_io_loop is ag_io_loop, "invalid current's asyncio ioloop object."


def main_thread_task():
	assert IOLoop.current(False) is None, "invalid current thread's ioloop object."

	io_loop = IOLoop()
	g_io_loop = IOLoop.instance()
	assert io_loop is not g_io_loop, "current ioloop object is the global ioloop object."

	try:
		a_io_loop = asyncio.get_event_loop()
	except RuntimeError:
		assert False, "incorrect asyncio event loop policy."

	return g_io_loop


def main():
	g_io_loop = main_thread_task()

	thread_list = []
	for idx in range(4):
		non_main_thread = threading.Thread(target=non_main_thread_task, args=(g_io_loop,))
		thread_list.append(non_main_thread)
		non_main_thread.start()

	for thread in thread_list:
		thread.join()

	print('Everything is ok...')


if __name__ == '__main__':
	main()
```

With the above code, we can see the behaviour about these discussions.
And you can get the file from gist [test_ioloop_construction_and_retrieve_in_multithread.py](https://gist.github.com/justdoit0823/91a0d3599a8aceb10367728a3665e2a3).


Reference
=========

  * <https://docs.python.org/3/library/asyncio-eventloops.html#event-loop-policies-and-the-default-policy>

  * <https://github.com/tornadoweb/tornado/blob/8e9e75502ff910629663c4cdd7779d43ea2dd150/tornado/ioloop.py#L116>

  * <https://github.com/tornadoweb/tornado/blob/8e9e75502ff910629663c4cdd7779d43ea2dd150/tornado/ioloop.py#L150>

  * <https://github.com/tornadoweb/tornado/blob/8e9e75502ff910629663c4cdd7779d43ea2dd150/tornado/ioloop.py#L194>
