
MySQL中间件Atlas
================


	Atlas是由 Qihoo 360公司Web平台部基础架构团队开发维护的一个基于MySQL协议的数据中间层项目。

	它在MySQL官方推出的MySQL-Proxy 0.8.2版本的基础上，修改了大量bug，添加了很多功能特性。



整体介绍
========


  * 开源情况


		代码开源发布在Github，有372分关注，1953个star，625个fork。

		有两个主干分支，master和sharding，master分支主要做功能正式发布，sharding分支做Atlas sharding方案。

		发布了11个release，同时有两位contributor。从提交纪录来看，该项目不是基于Github开发，导致open的issue较多，交流不及时。


  * 主要功能


	  * 读写分离

		
	  * 从库负载均衡


	  * IP过滤


	  * 自动分表


	  * DBA可平滑上下线DB

		
	  * 自动摘除宕机的DB


  * 对比官方MySQL-Proxy


	  * 将主流程中所有Lua代码用C重写，Lua仅用于管理接口

	  * 重写网络模型、线程模型

	  * 实现了真正意义上的连接池

	  * 优化了锁机制，性能提高数十倍


Atlas架构
=========


  * 整体架构


![Atlas总体架构图](https://camo.githubusercontent.com/42c01a1245183948ba8c61e5572d3aa9c3e8a08e/687474703a2f2f7777332e73696e61696d672e636e2f6c617267652f36653537303561356a7731656271353169336668716a32306a69306a6a7767392e6a7067)


	分析Client端发送过来的sql，根据既定策略把sql发到后面的MySQL实例。


  * 配置成HA的结构


![Atlas HA配置](https://camo.githubusercontent.com/4e602b6883556d3d33944871f76c2e23f8b229a2/687474703a2f2f7777342e73696e61696d672e636e2f6c617267652f36653537303561356a77316562713539766f39396e6a32306835306a39337a6d2e6a7067)


	数据库集群配置成一主多从，前端至少两台Atlas机器，通过LVS来做HA。


sharding方案
============


  * 单库分表（非Atlas Sharding方式）

		需要手动建表，且只支持hash分表，功能较弱。


  * Atlas Sharding


![Atlas Sharding](https://camo.githubusercontent.com/27c1cf8ccd7aafe18ac20c8bf1874192b4ac6850/687474703a2f2f7777312e73696e61696d672e636e2f6c617267652f36633034613030646a773165706d757267703778726a3230716f306b3061616c2e6a7067)


		支持多group，单个group为一主多从MySQL集群，可兼容第一种sharding方式。

		group切分支持两种模式，range和hash；range容易产生热点，hash适合均衡分布的查询。

		跨group功能支持较弱，只能正确支持CURD语句，不支持准确的聚合查询和事务。


实用功能
========

  * 读写分离和连接池管理，Atlas会将事务请求都发向主库，通过加注释/\*master*/可强制发向主库（不适合ORM）。

  * 读负载均衡，可以把主库也加入到读负载中，同时设置权重。非autocommit模式下的请求都会进主库，应用层要注意。

  * Proxy层做HA。

  * 主库宕机不影响读操作。

  * 通过管理接口进行后端DB上下线操作。


引用
====

  * [Atlas Github代码地址](https://github.com/Qihoo360/Atlas)

  * [Atlas wiki地址](https://github.com/Qihoo360/Atlas/wiki)
