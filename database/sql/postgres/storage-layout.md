
PostgreSQL Storage Layout Concepts
==================================

PostgreSQL存储概念主要包含Buffer, Block, Page, Tuple.


Block
=====

一个Block可以认为是一个基本的io单元，PostgreSQL中刚好是一个磁盘块。Block编号是有顺序的，从0到0xFFFFFFFE.

PostgreSQL中的relation或者index数据文件在内部会被切成相应多个的Block, 块数跟整个的数据长度有关。


Page
====

PostgreSQL中的Page是在Block基础上抽象而成的，整体结构如下所示：

```
 +----------------+---------------------------------+
 | PageHeaderData | linp1 linp2 linp3 ...           |
 +-----------+----+---------------------------------+
 | ... linpN |									  |
 +-----------+--------------------------------------+
 |		   ^ pd_lower							  |
 |												  |
 |			 v pd_upper							  |
 +-------------+------------------------------------+
 |			 | tupleN ...                         |
 +-------------+------------------+-----------------+
 |	   ... tuple3 tuple2 tuple1 | "special space" |
 +--------------------------------+-----------------+
									^ pd_special
```

包含一个header，接着是指向具体Tuple数据的line pointer；在尾部存在一个特殊的保留空间，然后就是实际的HeapTuple或者IndexTuple数据了。


Buffer
======


Buffer包含局部Buffer和共享Buffer，局部Buffer的索引从-1到-N，共享Buffer的索引从1到N。其中，0表示无效的Buffer.

同时，用BufferTag结构来存储Buffer存储对应的Block，具体结构定义在src/include/storage/buf_internals.h文件中。


从Page到Buffer
==============

写入Page数据到Buffer中时，根据Page信息构造BufferTag和要写入的Buffer索引值，记录到SharedBufHash表中。

通过Page信息，在全局SharedBufHash表中查找对应Buffer的索引值，然后读取缓存的Page数据。
