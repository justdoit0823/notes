docker
======
	docker是一种比VM更轻量级的容器软件，用于软件开发过程中环境的隔离和高效的部署。本文仅记录一下docker的基本原理。


docker的基本原理
================
	docker是基于linux内核所提供的的六大命名空间和权限管理机制来实现的。
	* 三个主要系统调用
		 * setns() 重新设置线程的命名空间,具体细节看setns(2)
		 * unshare() 控制进程的共享执行上下文，具体细节看unsahre(2)
		 * clone() 创建一个子进程，具体细节看clone(2)
	* 六大命名空间
		* IPC命名空间(CLONE_NEWIPC)
		* NET命名空间(CLONE_NEWNET)
		* UTS命名空间(CLONE_NEWUTS)
		* NS命名空间(CLONE_NEWNS)
		* PID命名空间(CLONE_NEWPID)
		* USER命名空间(CLONE_NEWUSER)
	* cgroups


docker的概念构成
================

	docker里面最终要的两部分就是image和container,image可以本地使用Dockerfile创建或者从docker hub拉取。


docker的使用
============

	在linux发行版下安装docker或者docker.io,然后运行相关命令就可以拉取或者创建image,有image之后就可以运行container等等。

docker的子命令
--------------

	我们可以利用bash补全或者help来查看docker全部的子命令。针对具体的子命令，一样会有帮助来说明怎么使用。

docker的自动化管理
==================

	docker-compose是使用python编写的来管理docker container的一个软件，通过编写docker-compose.yml文件来进行配置。


如何学习docker
==============

	* 首先得安装docker，然后各种折腾，熟悉命令。
	* 然后可以了解一些docker的具体使用，使用场景，部署场景。
	* 在使用的过程中，可以逐步地了解docker实现的根基。


docker文档
==========

	国内也有好多大牛写docker相关的文章，可以多看看。当然，官网是不能放过的，一个优秀的软件必须同时要有优秀的文档。

	文档链接:

	* <https://docs.docker.com/>
	* <http://dockerone.com/>

