Django管理事务细节
==================

Django针对集中不同的数据库，如MySQL, PostgreSQL等的操作进行了封装，实现了自己的ORM。
其中，针对可以提供事务功能的数据库，Django的ORM又提供了上下文管理器来进行方便的操作。


Python上下文的含义以及使用
--------------------------


上下文管理器提供了进入和退出上下文块的方法，\_\_enter\_\_和\_\_exit__来控制进入(如必要初始化)和退出(异常现场清理)时的动作。
在Python中，我们可以用with语法来方便地使用上下文管理。如打开文件:

	with open('file') as f:
		file_content = f.read()
		# do your business

使用上下文比较好的两点在于，

*  可以在\_\_enter__里面定制进入的一些特定动作，便于后续代码块的执行.

* 可以在\_\_exit__里面捕获代码块中的异常，进行必要的异常处理，让使用者无需关心细节。或者，针对不能正确处理的异常，可以向上抛出。

更多细节可以前往Python官方文档(<https://docs.python.org/3/reference/compound_stmts.html#the-with-statement>)进行查看。



Django中如何使用上下文管理器来操作事务
--------------------------------------

在Django的django/db目录下面有一个transaction模块, 里面提供了atomic方法，通过这样我们就可以愉快地开始使用事务了。

	with transaction.atomic():
		User.objects.filter(id=12345).update(name='test1')

通过简单地使用上下文管理器，就相当于在数据库中执行了一个事务。事务对应过程如下：

	BEGIN;
	update user set name='test1' where id=12345;
	COMMIT;

看起来相当方便，非常Pythonic，是不。



Django中事务管理器的细节
------------------------

* 事务管理器的细节

* 单个事务上下文管理器的使用

* 嵌套同数据库事务上下文管理器的使用

* 嵌套跨数据库事务上下文管理器的使用


### 事务管理器的细节 ###

通过transaction.atomic开启事务时，可以选择数据库和决定是否做savepoint。默认会使用配置文件中DATABASES中定义的default对应的数据库，在嵌套事务中会针对上一层做savepoint操作。
具体的事务过程如下：

* 初始化事务上下文管理器

		1) 通过using和savepoint参数来生成并且初始化一个Atomic对象.


* 执行进入事务块操作

		2) 执行1中得到的Atomic对象的\_\_enter\_\_方法，获取到指定数据库的连接，判断当前这个连接是否被标记为已经在事务块中。

		3) 在2中, 进入最外层事务块时, 标记数据库连接在事务块中, 自动提交为False; 如果已经关闭自动提交的话, 标记退出时自动提交为False并且标记该事务的数据库连接已经在事务块中(相当于把最外层数据块当做内层事务块额外做一遍4)中的操作, 并且在退出最外层事务块的时候有逻辑影响); 相反则标记为退出时自动提交为True。

		4) 在2中, 进入非最外层事务块时, 如果需要做savepoint且不用回滚的话, 做一次savepoint数据库操作, 并且把得到的sid存到事务数据库连接中的savepoint数组中; 相反则会把一个无效的sid给存到事务数据库连接中的savepoint数组中。


* 在事务块中针对数据库做DML操作

		5) 可以使用ORM提供的所有的针对数据库的操作, 需要注意的是, ORM操作中所使用的数据库连接必须是进入事务块时的数据库连接, 否则所做操作就不是在该事务中进行。如果没有进行连接指定, 数据库路由则会很隐蔽地影响事务过程。


* 执行退出事务块操作

		6) 退出事务块时, 先获取该事务的数据库连接, 通过对数据库连接的savepoint数组进行判断来确定是否在最外层事务, 如果是则标记该事务的数据库连接不在事务块中, 否则拿到该事务块最近的一次savepoint操作的sid。

		7) 如果事务的数据库连接以及关闭了, 则不用做任何事情, 数据库会在退出最外层事务块时自动回滚该事务。

		8) 如果事务块正常退出(没有发生异常和不需要回滚), 并且为非最外层事务块的话, 则针对6)中拿到的sid做savepoint释放操作(无效sid直接忽略), 出现数据库异常的话, 则回滚到未进入该事务块时的状态(如果继续异常的话, 则标记该事务的数据库连接需要回滚), 并把异常向上抛出。

		9) 如果事务块正常退出(没有发生异常和不需要回滚), 并且为最外层事务块的话, 则提交该事务; 出现异常的话, 则进行回滚操作(继续异常的话, 直接关闭该事务的数据库连接), 向上抛出异常。

		10) 如果不是7), 8), 9)中描述的情况, 标记该事务的数据库连接不需要回滚, 非最外层事务块的话, 如果6)中的sid有效，则回滚至该sid处的状态(异常则标记事务连接需要回滚), 否则标记事务连接需要回滚。

		11) 如果不是7), 8), 9)中描述的情况, 标记该事务的数据库连接不需要回滚, 最外层事务块的话, 直接进行事务回滚操作, 异常则关闭事务的数据库连接。

		12) 最后, 如果开启最外层事务时自动提交打开的话, 则对关闭的事务连接进行重置和打开自动提交; 否则, 则对关闭的事务连接进行重置和标记事务连接不在事务块中。


### 单个事务上下文管理器的使用 ###


一般地，在针对同一个数据库中多张表进行写操作时，会使用，保证数据的一致性。如：

	with transaction.atomic(using='db1'):
		A.objects.filter(id=123).update(value='value 1')
		B.objects.filter(id=456).update(value='value 2')


### 嵌套同数据库事务上下文管理器的使用 ###

本质上，同单个事务上下文管理器的使用没有什么区别，主要是多了一些保存点，可以进行部分事务的提交。
有可能是一些比较繁杂的逻辑过程中进行了拆分，针对每一个过程进行了事务管理,可能会造成全过程事务的不一致。如：

	with transaction.atomic(using='db1'):
		A.objects.filter(id=123).update(value='value 1')
		function1


	def function1():
		with transaction.atomic(using='db1'):
			B.objects.filter(id=789).update(value='value 3')
			C.objects.filter(id=321).update(value='value 4')


### 嵌套跨数据库事务上下文管理器的使用 ###

这种情况只能保证单个数据库的事务是完整的。针对于整个数据库操作过程来说，并没有完全完整，保证数据的一致性。
所以，这并不是一个好的使用方式。在PostgreSQL中，可以使用数据库提供的两阶段提交来实现这样事务操作，但是Django的ORM并没有实现这种功能。如：

	with transaction.atomic(using='db1'):
		B.objects.filter(id=1234).update(value='value o')
		C.objects.filter(id=2345).update(value='value x')
		function2

	def function2():
		with transaction.atomic(using='db2'):
			B.objects.filter(id=1000).update(value='value 7')
			C.objects.filter(id=2000).update(value='value 8')
