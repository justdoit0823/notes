
Coroutine
=========

About coroutine in Python, I have discussed at [The evolution of coroutine in Python](https://github.com/universe-proton/universe-topology/issues/12).
In this article, I will discuss more details about coroutine in tornado and asyncio. Before diving into the details, let's start with two examples.


Use coroutine in tornado,

```python
import functools

from tornado import gen, ioloop


@gen.coroutine
def foo(url):
    res = yield fetch_url(url)
    if res['code'] != 200:
        raise

    return res


@gen.coroutine
def fetch_url(url):
    return {'code': 200}


loop = ioloop.IOLoop().instance()
loop.run_sync(functools.partial(foo, 'https://foo.com'))
```


Use coroutine in asyncio,

```python
import asyncio


@asyncio.coroutine
def foo(url):
    res = yield from fetch_url(url)
    if res['code'] != 200:
        raise

    return res


@asyncio.coroutine
def fetch_url(url):
    return {'code': 200}


loop = asyncio.get_event_loop()
loop.run_until_complete(foo('https://foo.com'))
```

Or new style with `async` and `await`,

```python
import asyncio


async def foo(url):
    res = await fetch_url(url)
    if res['code'] != 200:
        raise

    return res


async def fetch_url(url):
    return {'code': 200}


loop = asyncio.get_event_loop()
loop.run_until_complete(foo('https://foo.com'))
```


It's obvious that tornado uses `yield` expression rather than `yield from` expression, which makes the root difference. I will talk about the reason later.


What's the real differences?
============================

Because the `yield` syntax doesn't support for controlling subiterator, the tornado must do much more work. Now take a look at how it works.


How `gen.coroutine` works?
--------------------------

Every function decorated with `gen.coroutine` returns a `Future` object, which is finished at the same time with the function.
From the most outer function to the most inner function, there may be a lot of decorated coroutines are yielded.
If the function is a common function, the future object is immediately finished with the function's return value as result.
After start, The coroutine will yield at the first unfinished future, which will be bound to the event loop.
Once the future is finished, the coroutine continues to execute and yields at the next unfinished future point, and so on.

Within this process, the future's result is backward propagated from the function which returns the future to the function which yields the future.
Future is the key point here. The execution pieces are linked together as a linear rope with a lot of futures. When the final future is finished, the whole process is done.

The `gen.coroutine` successfully simulates the `yield from` syntax at application level with the generator object and future object.
So we can write asynchronous functions as executing serially.


How `asyncio.coroutine` works?
--------------------------------

If the function is written with `yield from` syntax, the `asyncio.coroutine` just marks the function as an iterable coroutine at the bytecode level.
After start, the coroutine will yield as the same with the `gen.coroutine`, but the value of `yield from` is directly returned to the most outer caller.
For unfinished future, it's also bound to the event loop. Once the future is finished, the coroutine continues to execute with the result passed from the caller and yield at the next unfinished future point, and so on.

The future is returned from the inner subiterator to the most outer caller, and the result is passed from the most outer caller to the inner subiterator for the next time execution.
All these are driven by the `asyncio.Task` object.


Summary
-------

As the above, the general processes of the two are the same, but the `asyncio.coroutine` doesn't force the decorated function to return future object, which also unifies the most outer coroutine as the execution entry.
With the `yield from` syntax, the coroutine function's return value is automatically passed to the outer function, while tornado needs to do additional work to make the coroutine resumed at application level.
Meanwhile there are some performance benefits from native syntax by reducing application level coroutine scheduling and unnecessary future objects.

With the syntax `yield from`, it's easier for asyncio to implement cascaded coroutines which yield the future objects.


Why tornado doesn't work with yield from?
=========================================

I haven't asked this question in the community. But I have found somethings in tornado's change logs.
There have been a long time since the minimal prototype of coroutine was introduced in tornado.


The history of tornado's coroutine
------------------------------------

  * callback style

There is an example about writing an asynchronous handler in tornado.

```python
class AsyncHandler(RequestHandler):

    @asynchronous
    def get(self):
        http_client = AsyncHTTPClient()
        http_client.fetch("http://example.com",
            callback=self.on_fetch)

    def on_fetch(self, response):
        do_something_with_response(response)
        self.render("template.html")
```

At this time, tornado uses the callbacks to combine relative asynchronous functions together based on the low-level event loop.
With this style, the execution process of a function which contains asynchronous subroutines is divided into different parts with different contexts.
It's flexible for users, but difficult for the readers.

  * `gen`

The `gen` module was added in version 2.1 at Sep 20, 2011. While `yield from` was added in Python 3.3, and released on September 29, 2012. The new syntax is too late for tornado.
At that time, `yield` is the only mature choice. With `gen.engine` method to decorate asynchronous handler, we can yield asynchronous functions wrapped with `gen.Task` and think the task works serially.
So we don't need to care about the callbacks, but execution contexts are still separated. Although it's a good start for asynchronous functions with generator-based interface.

  * `gen.coroutine`

The `gen.coroutine` decorator was added as an alternative to `gen.engine` in version 3.0 at Mar 29, 2013. It supports calling asynchronous function serially.
And generator now yields `Future` objects rather than `gen.Task` objects. The same example is written in the new way.

```
class GenAsyncHandler(RequestHandler):

    @asynchronous
    @gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch("http://example.com")
        do_something_with_response(response)
        self.render("template.html")
```

This makes an enhancement about cascaded asynchronous functions. The `gen.Task` only solves one level yileding problem, and the later execution is still in the callback style way.
At this time, the `yield from` had been supported. But tornado still didn't use it. I think there may be two main reasons.

The first is compatibility. `yield from` syntax is only supported in Python 3.3 and the later versions, while `yield` is supported both in Python 2 and Python 3.
Adding any feature is needed to consider running both in Python 2 and 3, which is a huge cost and may make the development much harder.

The second is separation. At the initial time, writing in different ways with different Python versions is not wise. For users, it's not convenient; for committers, it's hard to maintain.
And any enhancement is only supported in Python 3, which benefits a little.


  * 5.0


But good news is that tornado 5.0 will support native coroutine. The details can be found at [Tornado 5.0 Status](https://groups.google.com/forum/#!topic/python-tornado/7JNWKwCTvZs).
Running native coroutine in tornado,

```python
import asyncio
import functools

from tornado import gen, ioloop


@asyncio.coroutine
def foo(url):
    res = yield from fetch_url(url)
    if res['code'] != 200:
        raise

    return res


@asyncio.coroutine
def fetch_url(url):
    return {'code': 200}


loop = ioloop.IOLoop().instance()
loop.run_sync(functools.partial(foo, 'https://foo.com'))
```

Or `async` style,

```python
import functools

from tornado import gen, ioloop


async def foo(url):
    res = await fetch_url(url)
    if res['code'] != 200:
        raise

    return res


async def fetch_url(url):
    return {'code': 200}


loop = ioloop.IOLoop().instance()
loop.run_sync(functools.partial(foo, 'https://foo.com'))
```

We can try the above codes with tornado on [bdarnell/asyncio-future](https://github.com/bdarnell/tornado/tree/asyncio-future) branch.


According to the history, tornado has been also improved so much, and also keeps up to with the standard library implemention.


Reference
=========

  * <http://www.tornadoweb.org/en/stable/releases.html>

  * <https://docs.python.org/3/whatsnew/index.html>

  * <https://groups.google.com/forum/#!topic/python-tornado/7JNWKwCTvZs>

