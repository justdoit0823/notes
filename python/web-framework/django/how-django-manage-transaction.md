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

3) 在2中，如果不在事务块中(进入最外层事务块时),标记在退出上下文时提交，标记连接不需要回滚.


4) 针对一些在关闭自动提交时，不能正常处理事务提交和savepoint的数据库，标记连接在事务块中，并且在标记在退出上下文的时候不提交。

5) 如果此时连接被标记为在事务块中时，并且需要进行savepoint操作和连接不需要回滚时，做一次savepoint操作，
拿到一个savepoint ID, 并且加到连接维护的savepoint列表中;反之，则加一个无效的savepoint ID到保存点列表中。

6) 如果此时连接没有被标记在事务块中时，标记连接在事务块中，并且关闭自动提交。

7) 在事务块中针对数据库做DML操作。


* 执行退出事务块操作

8) 退出事务块时，先获取进入此事务块时指定的数据库连接, 判断该连接是否还有保存点,如果有，取出最后一次做savepoint操作的保存点;反之，则标记连接退出事务块(最外层的事务退出)。

9) 如果连接在事务过程中被关闭了，那么数据库会自己做回滚，应用无需关心。

10) 如果正常退出事务块，并且连接不需要回滚, 如果连接在事务块中，不是最外层事务块，则尝试释放保存点.释放失败的话，则尝试回滚至保存点(回滚失败的话，标记连接需要回滚), 向上抛出异常。

11) 如果是最外层事务块退出，则尝试提交事务，失败的话尝试回滚事务(回滚失败的话，关闭连接),向上抛出异常。

12) 如果异常退出事务块,先标记连接不需要回滚，如果连接标记为在事务块中,保存点无效的话，标记连接需要回滚；有效的话，尝试回滚至保存点(回滚失败的话，标记连接需要回滚).

13) 如果连接退出最外层事务块，尝试进行事务回滚操作, 失败的话关系连接.

14) 支持自动提交的话，在最外层事务块退出时,如果连接在事务中关闭的话，重置连接；其它情况下，打开自动提交。

15) 不支持自动提交的话，在最外层事务块退出时，如果连接在事务中关闭的话，重置连接；其它情况下，标记连接退出事务块。

16) 针对任何事务块内发生的异常，事务管理器都会往上层抛出。


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
