

Uber switch PostgreSQL to MySQL
===============================

	[原文](https://eng.uber.com/mysql-migration/)出自uber官方博客上面的一篇文章。



PostgreSQL的不足
================

  * 架构导致的写效率不高

  * 数据复制效率不高
  
  * 数据表的损坏问题

  * 备机MVCC支持不好

  * 难以升级到新版本（跨大版本 ）



PostgreSQL与MySQL的实现对比
===========================

  * 索引寻址不同

		PostgreSQL中通过ctid找到行对应的物理位置，每一个索引队都是直接存储ctid，然后来寻址的;

		而MySQL则是通过主键来寻址到行的物理位置，然后次级索引都是指向主键。

		同时PostgreSQL的插入又是通过新插行来实现的，导致每一次非索引列的更新都要对索引进行更新，从而放大了写的量。

		但是文章中举例一个表建12个索引，来说明事情的严重性，我觉得也很上天。

		另外这也是InnoDB引擎没有主键的时候表现得很傻的原因所在吧。

		
  * 复制方式不同

		PostgreSQL在9.4之前不支持逻辑复制，只支持物理服务;而MySQL支持逻辑复制。简单带过MySQL复制会丢数据，而大话PostgreSQL会损坏表。

		另外提到的升级难的问题，也只是PostgreSQL9.4之前的事了。


  * 备机MVCC支持差

		由于实现原因，PostgreSQL standby上面不能完全支持MVCC，但是作者引用的2ndQuadrant博客文章也说得很明白了，如下：

		A HOT update or VACUUM related update arrives to delete something that query expects to be visible

		A B-tree deletion appears

		There is a locking issue between the query you’re running and what locks are required for the update to be processed

		关于锁的问题，文章里面也说了在备库只读的情况下，一般很难发生。另外两个只是有可能导致查询被中断取消。

		PostgreSQL官方文档里面也提到了在standby上面可能发生的冲突问题，继而导致的备库落后主库，但是都是可以通过参数来调节，并且在应用层做优化的。

		不是每一次查询都是要用一个30秒的transaction来完成的，然后文中举的发邮件的例子太可爱了。非得按照的错误的方式做，还要把锅扔给工具。

  * WAL日志的量太大

		这个一开始选PostgreSQL的时候不知道，另外传输的时候可以压缩吧。

  * 数据损坏

		有bug了还不升级，想什么呢。


  * 升级难

		升级到9.4之后不就都好了，非得在9.2上面耗着。当然夸大版本升级也确实比较坑，不过应该还是能想到办法的。

  * 连接问题

		这个真是给跪了，用pgbouncer还能在代码里面搞出连接泄漏的bug，这也要怪PostgreSQL。

  * 缓存

		这个没怎么研究，不太懂。



总结
====


  * 例子举得比较荒唐，没有什么说服力


  * 可以当作知识来学学，结论别太当真


  * PostgreSQL都快要发布9.6了，作者还这儿通过将9.2的一些问题来说PostgreSQL不如MySQL



引用
====

  * <https://eng.uber.com/mysql-migration/>

  * <http://blog.2ndquadrant.com/tradeoffs_in_hot_standby_deplo/>

  * <https://www.postgresql.org/docs/devel/static/hot-standby.html>
