Django处理请求过程的细节
========================


此文档主要是针对Django在处理请求的过程中，一些实现细节上的讨论。主要涉及解析请求,
中间件的加载，信号的发送,路由的映射，具体请求的执行逻辑，到返回响应。
与运行容器的交互细节在此略过。


[WSGI容器调用的入口](#WSGI容器调用的入口)

[中间件的加载过程](#中间件的加载过程)

[初始化路由决策和进行路由映射分配](#初始化路由决策和进行路由映射分配)

[执行具体请求逻辑](#执行具体请求逻辑)

[返回处理逻辑得到的响应](#返回处理逻辑得到的响应)


WSGI容器调用的入口
------------------

在django.core.handlers包中有两个重要模块base和wsgi, 前者主要是设计实现了一个处理请求的基类BaseHandler,封装处理了主要的过程,方便适配不同的协议调用。
而后者继承BaseHandler实现了WSGIHandler, 并且实现了\_\_call\_\_调用,使得该handler实例能够被用来回调。详细代码如下：

	class WSGIHandler(base.BaseHandler):
		initLock = Lock()
		request_class = WSGIRequest

		def __call__(self, environ, start_response):
			# Set up middleware if needed. We couldn't do this earlier, because
			# settings weren't available.
			if self._request_middleware is None:
				with self.initLock:
					try:
						# Check that middleware is still uninitialized.
						if self._request_middleware is None:
							self.load_middleware()
					except:
						# Unload whatever middleware we got
						self._request_middleware = None
						raise

			set_script_prefix(get_script_name(environ))
			signals.request_started.send(sender=self.__class__)
			try:
				request = self.request_class(environ)
			except UnicodeDecodeError:
				logger.warning('Bad Request (UnicodeDecodeError)',
					exc_info=sys.exc_info(),
					extra={
						'status_code': 400,
					}
				)
				response = http.HttpResponseBadRequest()
			else:
				response = self.get_response(request)

			response._handler_class = self.__class__

			status = '%s %s' % (response.status_code, response.reason_phrase)
			response_headers = [(str(k), str(v)) for k, v in response.items()]
			for c in response.cookies.values():
				response_headers.append((str('Set-Cookie'), str(c.output(header=''))))
			start_response(force_str(status), response_headers)
			return response

如上代码所示，在获得环境变量和处理响应(回送到运行容器)的回调后，会首先进行请求中间件的初始化，注意该初始化只会在没有加载任何请求中间件的时候才会进行，一般只是首次加载。
另外，Django自己设计实现了一些过程节点的信号，可用于钩子来进行阶段处理。如请求开始，请求结束，请求异常等。在加载中间件完毕后会发送请求开始的信号，然后解析环境变量，构造请求实例，进行请求处理。


中间件的加载过程
----------------

Django定义了五种中间件，分别为请求中间件，模板中间件，视图中间件，响应中间件，异常中间件。中间件是一个普通的类，只不过针对不同类型的中间件，需要分别定义不同的方法。
请求中间件需要定义process\_request方法, 模板中间件需要定义process\_template\_response方法, 视图中间件需要定义process\_view方法，响应中间件需要定义process\_response方法,
异常中间件需要定义process\_exception方法。一个类可以同时属于多种中间件，即同时定义多种方法。另外，不同中间件的执行顺序是不一样的,
请求中间件和视图中间件是按照在MIDDLEWARE\_CLASSES变量中定义的顺序执行的，模板中间件、响应中间件和异常中间件是按照在变量中定义的顺序逆序执行的。

	class ExampleMiddleware(object):

	    def process_request(self, request):
			# handle request

	    def process_template_response(self, request, response):
			# handle template response

	    def process_view(self, request, callback, callback_args, callback_kwargs):
			# handle view

	    def process_response(self, request, response):
			# handle response

	    def process_exception(self, request, e):
		    # handle exception


初始化路由决策和进行路由映射分配
--------------------------------

初始化路由决策，首先执行请求中间件，如果没有响应的话，根据请求的路径进行路由映射分析，获取匹配参数(主要是正则表达式中的匹配值)，然后执行视图中间件,
如果没有响应的话，根据映射执行请求处理逻辑，在处理逻辑过程中如有异常抛出的话，会执行异常中间件，
进行应用定义的异常处理, 如果应用定义的异常中间件没有响应返回的话，此处会把异常向上抛出，并发送对应的异常信号。
在正常返回响应的情况下，如果响应支持模板渲染，则会执行模板响应中间件。最后，执行响应中间件，并返回响应,
如果异常，会执行handle\_uncaught\_exception方法进行最终异常处理。

    def get_response(self, request):
        "Returns an HttpResponse object for the given HttpRequest"

        # Setup default url resolver for this thread, this code is outside
        # the try/except so we don't get a spurious "unbound local
        # variable" exception in the event an exception is raised before
        # resolver is set
        urlconf = settings.ROOT_URLCONF
        urlresolvers.set_urlconf(urlconf)
        resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)
        try:
            response = None
            # Apply request middleware
            for middleware_method in self._request_middleware:
                response = middleware_method(request)
                if response:
                    break

            if response is None:
                if hasattr(request, 'urlconf'):
                    # Reset url resolver with a custom urlconf.
                    urlconf = request.urlconf
                    urlresolvers.set_urlconf(urlconf)
                    resolver = urlresolvers.RegexURLResolver(r'^/', urlconf)

                resolver_match = resolver.resolve(request.path_info)
                callback, callback_args, callback_kwargs = resolver_match
                request.resolver_match = resolver_match

                # Apply view middleware
                for middleware_method in self._view_middleware:
                    response = middleware_method(request, callback, callback_args, callback_kwargs)
                    if response:
                        break

            if response is None:
                wrapped_callback = self.make_view_atomic(callback)
                try:
                    response = wrapped_callback(request, *callback_args, **callback_kwargs)
                except Exception as e:
                    # If the view raised an exception, run it through exception
                    # middleware, and if the exception middleware returns a
                    # response, use that. Otherwise, reraise the exception.
                    for middleware_method in self._exception_middleware:
                        response = middleware_method(request, e)
                        if response:
                            break
                    if response is None:
                        raise

            # Complain if the view returned None (a common error).
            if response is None:
                if isinstance(callback, types.FunctionType):    # FBV
                    view_name = callback.__name__
                else:                                           # CBV
                    view_name = callback.__class__.__name__ + '.__call__'
                raise ValueError("The view %s.%s didn't return an HttpResponse object. It returned None instead."
                                 % (callback.__module__, view_name))

            # If the response supports deferred rendering, apply template
            # response middleware and then render the response
            if hasattr(response, 'render') and callable(response.render):
                for middleware_method in self._template_response_middleware:
                    response = middleware_method(request, response)
                response = response.render()

        except http.Http404 as e:
            logger.warning('Not Found: %s', request.path,
                        extra={
                            'status_code': 404,
                            'request': request
                        })
            if settings.DEBUG:
                response = debug.technical_404_response(request, e)
            else:
                try:
                    callback, param_dict = resolver.resolve404()
                    response = callback(request, **param_dict)
                except:
                    signals.got_request_exception.send(sender=self.__class__, request=request)
                    response = self.handle_uncaught_exception(request, resolver, sys.exc_info())

        except PermissionDenied:
            logger.warning(
                'Forbidden (Permission denied): %s', request.path,
                extra={
                    'status_code': 403,
                    'request': request
                })
            try:
                callback, param_dict = resolver.resolve403()
                response = callback(request, **param_dict)
            except:
                signals.got_request_exception.send(
                    sender=self.__class__, request=request)
                response = self.handle_uncaught_exception(request,
                    resolver, sys.exc_info())

        except SuspiciousOperation as e:
            # The request logger receives events for any problematic request
            # The security logger receives events for all SuspiciousOperations
            security_logger = logging.getLogger('django.security.%s' %
                            e.__class__.__name__)
            security_logger.error(
                force_text(e),
                extra={
                    'status_code': 400,
                    'request': request
                })

            try:
                callback, param_dict = resolver.resolve400()
                response = callback(request, **param_dict)
            except:
                signals.got_request_exception.send(
                    sender=self.__class__, request=request)
                response = self.handle_uncaught_exception(request,
                    resolver, sys.exc_info())

        except SystemExit:
            # Allow sys.exit() to actually exit. See tickets #1023 and #4701
            raise

        except:  # Handle everything else.
            # Get the exception info now, in case another exception is thrown later.
            signals.got_request_exception.send(sender=self.__class__, request=request)
            response = self.handle_uncaught_exception(request, resolver, sys.exc_info())

        try:
            # Apply response middleware, regardless of the response
            for middleware_method in self._response_middleware:
                response = middleware_method(request, response)
            response = self.apply_response_fixes(request, response)
        except:  # Any exception should be gathered and handled
            signals.got_request_exception.send(sender=self.__class__, request=request)
            response = self.handle_uncaught_exception(request, resolver, sys.exc_info())

        response._closable_objects.append(request)

        return response


执行具体请求逻辑
----------------

定义处理请求的方法，然后根据不同的需要，实现不同的逻辑，并返回响应。如：

	def index(request, *args, **kwargs):

	    # handle request
		return HttpResponse('index')


返回处理逻辑得到的响应
----------------------

写响应状态，响应头，应用定义的cookie，并回送响应给容器调用.
