
Celery
======

Celery is a simple, flexible, and reliable distributed system to process vast amounts of messages,

while providing operations with the tools required to maintain such a system.


Reliablity Stratege
===================


Default
-------

Task is acknowledged after accepted.

```
def on_accepted(self, pid, time_accepted):
	"""Handler called when task is accepted by worker pool."""
	self.worker_pid = pid
	self.time_start = time_accepted
	task_accepted(self)
	if not self.task.acks_late:
		self.acknowledge()
	self.send_event('task-started')
	if _does_debug:
		debug('Task accepted: %s[%s] pid:%r', self.name, self.id, pid)
	if self._terminate_on_ack is not None:
		self.terminate(*self._terminate_on_ack)
```

Retry
-----

When set autoretry_for argument in task decorator, celery will automatically retry the task.

```
def _task_from_fun(self, fun, name=None, base=None, bind=False, **options):
	if not self.finalized and not self.autofinalize:
		raise RuntimeError('Contract breach: app not finalized')
	name = name or self.gen_task_name(fun.__name__, fun.__module__)
	base = base or self.Task

	if name not in self._tasks:
		run = fun if bind else staticmethod(fun)
		task = type(fun.__name__, (base,), dict({
			'app': self,
			'name': name,
			'run': run,
			'_decorated': True,
			'__doc__': fun.__doc__,
			'__module__': fun.__module__,
			'__header__': staticmethod(head_from_fun(fun, bound=bind)),
			'__wrapped__': run}, **options))()
		# for some reason __qualname__ cannot be set in type()
		# so we have to set it here.
		try:
			task.__qualname__ = fun.__qualname__
		except AttributeError:
			pass
		self._tasks[task.name] = task
		task.bind(self)  # connects task to this app

		autoretry_for = tuple(options.get('autoretry_for', ()))
		retry_kwargs = options.get('retry_kwargs', {})

		if autoretry_for and not hasattr(task, '_orig_run'):

			@wraps(task.run)
			def run(*args, **kwargs):
				try:
					return task._orig_run(*args, **kwargs)
				except autoretry_for as exc:
					raise task.retry(exc=exc, **retry_kwargs)

			task._orig_run, task.run = task.run, run
	else:
		task = self._tasks[name]
	return task

```


Late Ack
--------

Task is acknowledged after executed. Whether success

```
def on_success(self, failed__retval__runtime, **kwargs):
	"""Handler called if the task was successfully processed."""
	failed, retval, runtime = failed__retval__runtime
	if failed:
		if isinstance(retval.exception, (SystemExit, KeyboardInterrupt)):
			raise retval.exception
		return self.on_failure(retval, return_ok=True)
	task_ready(self)

	if self.task.acks_late:
		self.acknowledge()

	self.send_event('task-succeeded', result=retval, runtime=runtime)

```


or failure(task exception or worker lost),

```
def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
	"""Handler called if the task raised an exception."""
	task_ready(self)
	if isinstance(exc_info.exception, MemoryError):
		raise MemoryError('Process got: %s' % (exc_info.exception,))
	elif isinstance(exc_info.exception, Reject):
		return self.reject(requeue=exc_info.exception.requeue)
	elif isinstance(exc_info.exception, Ignore):
		return self.acknowledge()

	exc = exc_info.exception

	if isinstance(exc, Retry):
		return self.on_retry(exc_info)

	# These are special cases where the process wouldn't've had
	# time to write the result.
	if isinstance(exc, Terminated):
		self._announce_revoked(
			'terminated', True, string(exc), False)
		send_failed_event = False  # already sent revoked event
	elif isinstance(exc, WorkerLostError) or not return_ok:
		self.task.backend.mark_as_failure(
			self.id, exc, request=self, store_result=self.store_errors,
		)
	# (acks_late) acknowledge after result stored.
	if self.task.acks_late:
		requeue = not self.delivery_info.get('redelivered')
		reject = (
			self.task.reject_on_worker_lost and
			isinstance(exc, WorkerLostError)
		)
		if reject:
			self.reject(requeue=requeue)
			send_failed_event = False
		else:
			self.acknowledge()

	if send_failed_event:
		self.send_event(
			'task-failed',
			exception=safe_repr(get_pickled_exception(exc_info.exception)),
			traceback=exc_info.traceback,
		)

	if not return_ok:
		error('Task handler raised error: %r', exc,
			  exc_info=exc_info.exc_info)
```


Task reject on worker lost
--------------------------

When worker has abruptly exited, the task won't be acknowledged, and be requeue later.


Reference
=========

  * <http://docs.celeryproject.org/en/latest/userguide/tasks.html>
