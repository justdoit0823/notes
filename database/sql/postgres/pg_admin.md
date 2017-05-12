PostgreSQL运维文档
==================

* [数据库初始化操作](#数据库初始化操作)

* [数据库运行操作](#数据库运行操作)

* [数据库备份](#数据库备份)



数据库初始化操作
----------------

* 初始化PostgreSQL

		initdb --encoding=utf8 --locale=zh_CN.UTF-8 /home/postgres/db0/data


* 创建数据库

		createdb -h 192.168.1.21 -U postgres --encoding=utf8 --locale=zh_CN.UTF-8 dbname


* 创建PostgreSQL用户

		createuser -d -E -l -P -r -s rolename



数据库运行操作
--------------

* 启动PostgreSQL Server

		export PGDATA="/home/postgres/db0/data"

		pg_ctl start

		pg_ctl -D /home/postgres/db0/data start


* 停止PostgreSQL Server

		export PGDATA="/home/postgres/db0/data"

		pg_ctl stop

		pg_ctl -D /home/postgres/db0/data stop


* 重启PostgreSQL Server

		export PGDATA="/home/postgres/db0/data"

		pg_ctl restart

		pg_ctl -D /home/postgres/db0/data restart


数据库备份
----------


* 全库物理备份

		pg_basebackup -h 192.168.1.21 -U replication -F t -P -x -R -D /home/postgres/pgdata -l backup201507131613

		cd $PGDATA

		tar -xf base.tar -C ./

		pg_ctl start


* 全库逻辑备份

		pg_dump -h 192.168.1.21 -U postgres -j 4 -F t -C -f /home/postgresql/dump.sql dbname (单库并行备份)

		pg_restore -h 192.168.1.21 -U postgres -j 4 -C -d dbname /home/postgresql/dump.sql (单库并行导入)
