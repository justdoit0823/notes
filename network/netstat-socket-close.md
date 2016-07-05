

netstat中显示open socket时进程ID的变化
======================================


	netstat命令中存在－p选项可以显示出当前socket所属的进程ID和进程名字


* 命令选项

		-p, --program
		Show the PID and name of the program to which each socket belongs.


* 内容解释

		PID/Program name
		Slash-separated  pair  of  the process id (PID) and process name of the process that owns the socket.



不同情形下进程ID的变化
======================



  * socket结束过程


		socket处于ESTABLISHED状态时，引发TCP主动结束过程，在TIME_WAIT时间内仍然显示，但无进程信息，TIME_WAIT时间后netstat不再显示。

		socket处于CLOSE_WAIT状态时，引发TCP被动结束过程，netstat不再显示。



  * socket只在单个进程内


		进程退出时，主动释放socket file descriptor，执行socket结束过程。


		如果未退出，只是调用close，存在复制情况下，netstat正常显示；无复制情况下，执行socket结束过程。


  * socket在主进程中被创建，主进程中又fork

		主进程存在时，netstat显示的仍然是主进程的pid。

		主进程退出，netstat中显示的pid就变成了子进程的pid，并且无TCP主动结束过程。

		子进程先退出，netstat显示无变化。

		父子进程都退出后，执行socket结束过程。


  * socket在主进程中被创建，主进程多次fork

		主进程存在时，netstat显示的仍然是主进程的pid。

		主进程退出，netstat中显示的pid变成了活着的子进程中选择(看到的是按子进程创建顺序来转移的，不确定具体实现)的一个pid，并且无TCP主动结束过程。

		子进程退出，netstat显示无变化。

		所有父子进程都退出后，执行socket结束过程。


close和shutdown的区别
=====================

  * close

		只是减少socket file descriptor的引用计数，只有当引用计数为0时才引发TCP主动结束过程(不存在半连接)。


  * shutdown

		直接引发TCP结束过程(存在半连接)。


进程退出和exit
==============

  * man 2 exit

		The  function  _exit()  terminates  the  calling process "immediately".

		Any open file descriptors belonging to the process are closed;

		any children of the process are inherited by process 1,

		init, and the process's parent is sent a SIGCHLD signal.



测试代码
========

  * Python版

		import socket
		import os
		import time
		import sys


		def test_socket_netstat(host, port):
			c1 = socket.socket()
			print('connect to host ', host, ' at port ', port)
			c1.connect((host, port))
			print('local sock name ', c1.getsockname())
			pid = os.fork()
			if pid == 0:
				# child process
				while True:
					time.sleep(2)
			else:
				# parent process
				while True:
					time.sleep(1)


		def main():
			host = sys.argv[1]
			port = int(sys.argv[2])
			test_socket_netstat(host, port)


		if __name__ == '__main__':
			main()


  * C版

		#include "stdio.h"
		#include "unistd.h"
		#include <sys/types.h>
		#include <sys/socket.h>
		#include <netinet/in.h>
		#include <arpa/inet.h>
		#include <stdlib.h>


		int main(int argc, char * argv[]){
		  char * host = argv[1];
		  int port = atoi(argv[2]);
		  struct sockaddr_in addr_in;
		  pid_t pid, tpid;
		  int cfd;
		  cfd = socket(AF_INET, SOCK_STREAM, 0);
		  addr_in.sin_family = AF_INET;
		  addr_in.sin_port = htons(port);
		  inet_aton(host, &addr_in.sin_addr);
		  connect(cfd, (struct sockaddr *)&addr_in, sizeof(struct sockaddr_in));
		  printf("connect to host %s at port %d...\n", host, port);
		  pid = fork();
		  if(pid == -1){
			exit(0);
		  }

		  if(pid == 0){
			while(1){
			  sleep(2);
			}
		  }
		  else{
			tpid = fork();
			if(tpid == -1){
			  printf("fork failed...\n");
			  exit(0);
			}

			if(tpid == 0){
			  while(1){
			sleep(2);
			  }
			}
			else{
			  while(1){
			sleep(1);
			  }
			}
		  }
		  printf("end....\n");
		}
