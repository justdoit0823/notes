
#include "stdio.h"
#include "unistd.h"
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>
#include <poll.h>
#include <pthread.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>


int setnonblocking(int fd){
  int flag, ret;
  flag = fcntl(fd, F_GETFL, NULL);
  flag |= O_NONBLOCK;
  ret = fcntl(fd, F_SETFL, flag);
  return ret;
}


int start_listen_server(const char * host, int port){
  int s_sock, flag;
  struct sockaddr_in addr;
  printf("host %s, port %d\n", host, port);
  memset(&addr, 0, sizeof(addr));
  inet_aton(host, &addr.sin_addr);
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  s_sock = socket(AF_INET, SOCK_STREAM, 0);
  flag = 1;
  setsockopt(s_sock, SOL_SOCKET, SO_REUSEADDR, &flag, sizeof(flag));
  setnonblocking(s_sock);
  bind(s_sock, (struct sockaddr *)&addr, sizeof(struct sockaddr));
  listen(s_sock, 5);
  return s_sock;
}


void * poll_loop(void * args){
  int ret, conn_sock, listen_sock, addrlen, id;
  struct sockaddr_in addr;
  struct pollfd p_buf[1];
  
  listen_sock = ((int *)args)[0];
  p_buf[0].fd = listen_sock;
  p_buf[0].events = POLLIN;
  id = pthread_self();
  
  while(1){
    printf("waiting for poll.\n");
    ret = poll(p_buf, 1, -1);
    if(ret == -1){
      printf("poll errror.\n");
      return;
    }

    printf("poll success in thread %u.\n", id);
    break;
  }
}


int run_server(int argc, char * argv[]){
  int server_sock, pid;
  pthread_t thread1, thread2;
  int args[1];

  server_sock = start_listen_server(argv[1], atoi(argv[2]));
  args[0] = server_sock;

  pthread_create(&thread1, NULL, poll_loop, &args[0]);
  pthread_create(&thread2, NULL, poll_loop, &args[0]);

  pthread_join(thread1, NULL);
  pthread_join(thread2, NULL);

  return 0;
}


int main(int argc, char * argv[]){
  run_server(argc, argv);
}
