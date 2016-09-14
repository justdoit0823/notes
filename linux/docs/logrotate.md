
Logrotate
=========

	logrotate is designed to ease administration of systems that generate large numbers of log files.

	It allows automatic rotation, compression, removal, and mailing of log files.

	Each log file may be handled daily, weekly, monthly, or when it grows too large.


运行
====

	一般地，logrotate以定时任务的形式运行，可以自己定制crontab或者使用anacrontab.


  * 脚本位置

		/etc/cron.daily/logrotate

  * crontab

		把脚本移到别的位置，然后配置crontab启动。

  * anacrontab

		修改anacrontab里面的配置项，如运行时间，延迟时间等。


配置
========

  * 新增配置


		在/etc/logrotate.d/目录中新增需要切割的日志配置，如:

		/path/access.log
		{
			copytruncate
			create works works
			daily
			dateext
			dateyesterday
			maxsize 100M
			missingok
			nomail
			rotate 7
			su works works
		}

  * 测试配置结果


		用debug模式运行logrotate, 如: logrotate -d /etc/logrotate.d/app


潜在问题
========

	对于不支持日志切换交互过程的程序来说，可能存在日志丢失。反之，可以在配置中定义交互过程脚本块。


手册
====

  * man logrotate

  * man crontab

  * man anacrontab
