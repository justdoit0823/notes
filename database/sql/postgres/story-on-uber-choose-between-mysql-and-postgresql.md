
Uber工程师抛出长文
======================

	Uber工程师Evan Klitzke7月26日在官方blog上面发出长文，列举Uber从PostgreSQL迁移到MySQL的罪证。

	主要问题如下：

	1. 架构导致的写效率不行, 主要表现在更新Tuple非索引列的时候，表里面的所有索引都有写入负担。

	2. 复制效率不行，主要表现在WAL log产生得太多，跟1也有关系。

	3. Standby上面的MVCC机制不完善，表现在读写存在数据竞争。

	4. 难以跨大版本升级。


事件持续发酵
============

  * HackerNews转推上文

  * 微博上也是各种讨论

  * 知乎上面的问题帖都发出来了


圈内人的回应
============


Robert Haas
-----------


PostgreSQL的核心开发者，EnterpriseDB的首席架构师在blogspot上面发表了自己的看法，写得很平和谦虚。主要观点如下：


	Uber的文章说明PostgreSQL还有很多改进的地方。

	虽然没有强烈的反击，但是言语之中却也指出了Uber工程师文中的一些问题。

	如PostgreSQL非索引列时的HOT功能，InnoDB中可能存在的空间效率不高和聚集索引带来的非主键索引访问效率问题，

	以及在索引多和更新很频繁的场景下，InnoDB很难一定更有效。WAL log的可压缩或者ssl传输。针对standby上面的MVCC问题，可以配置hot_standby_feedback=on基本缓解。

	逻辑复制在9.4版本之后已经支持，以及可以用pglogical, Slony, Bucardo, Londiste 或者 xDB Replication Server工具等。

	开发新的Tuple格式，但是同样存在社区维护上的问题。如开发资源的分裂，PostgreSQL版本的分裂等。

	回顾了一下PostgreSQL近年来所取得的很多进步; 同时还指出，不管进步了多少，还是有那么多问题。


Simon Riggs
-----------

PostgreSQL的核心开发者，2ndQuadrant的工程师在自家的官方blog上也来了一篇，就没那么客气了。主要观点如下：


	Uber的文章只指出了事情的一面，并没有点出另外一面。

	standby的MVCC也是可以通过配置参数来解决的。

	指出PostgreSQL索引的直接访问对查询来比InnoDB的索引间接访问更有优势，

	而且大多数情况下写btree索引结构的时候性能差不多。

	另外，索引的访问方式没有什么架构继承性上的约束，可以进行改进。

	最后，针对复制当然要推一把自家的pglogical和一些几乎无缝的在线升级服务。


后续
====

  * Why we lost Uber as a user


		以此为主题的邮件在PostgreSQL的官方邮件列表里进行了热烈的讨论，大有要做出改变的想法。


  * Heap WARM Tuples - Design Draft


		2ndQuadrant的工程师Pavan Deolasee已经发起了优化草案，给出了详细的实现思路，

		主要是避免更新Tuple的时候过多地写入索引.看来是要维护好“最好的开源数据库”这个荣耀啊。


番外
====

	Uber工程师Evan Klitzke在2013年从MySQL迁移到了PostgreSQL，主要需求是想用PostGIS。

	同样balabala一堆迁移的痛苦，各种类型转换，约束等等细节的东西。

	微博上面还各种评论是不是换上级了，同时PostgreSQL的核心开发者在邮件列表里也指出了部分跟uber新换了CTO有关，哈哈。

	另外，搜了一些这哥们儿的twitter主页，并没有看到写什么首席架构师，技术VP什么的。


评论
====

	说实话，虽然Evan Klitzke点出了一些技术细节，但是没太写出水准。给出的细节太少，举的例子完全有失水准。
