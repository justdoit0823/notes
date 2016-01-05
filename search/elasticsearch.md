
elasticsearch模型结构
=====================

特点
----

* 无固定关系结构

* 文档存储

* 分布式

* Restful接口操作

* 可复制

* 可分片



节点拓扑
--------

* 节点类型

		分主从节点, 针对于复制来说。

* 节点分布

		以分布式集群存在


索引
-----

* 类型(mapping)

		索引的逻辑分组


* 字段(field)

		文档中的基本组成

* 逻辑结构

		index -> mapping -> field
		单个索引包含至少一个mapping, 单个mapping中包含若干字段，每个字段包含自己的属性，字段作为mapping的属性出现。



文档
----

	mapping的实例化对象,实际存储在索引里面的东西。


Restful接口格式
---------------

* 动作

		GET POST PUT DELETE

* 格式

		/index_name/mapping_name/document_id


Reference
=========

* <https://www.elastic.co/guide/en/elasticsearch/reference/current/_basic_concepts.html>
