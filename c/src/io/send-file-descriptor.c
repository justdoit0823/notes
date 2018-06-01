
#include <arpa/inet.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>


static void send_fd(int socket, int fd) {
  struct msghdr msg = { 0 };
  char buf[CMSG_SPACE(sizeof(fd))];
  memset(buf, '\0', sizeof(buf));
  struct iovec io = { .iov_base = "ABC", .iov_len = 3 };

  msg.msg_iov = &io;
  msg.msg_iovlen = 1;
  msg.msg_control = buf;
  msg.msg_controllen = sizeof(buf);

  struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
  cmsg->cmsg_level = SOL_SOCKET;
  cmsg->cmsg_type = SCM_RIGHTS;
  cmsg->cmsg_len = CMSG_LEN(sizeof(fd));

  *((int *) CMSG_DATA(cmsg)) = fd;

  msg.msg_controllen = cmsg->cmsg_len;

  if (sendmsg(socket, &msg, 0) < 0) printf("Failed to send message\n");

}

static int recv_fd(int socket) {
  struct msghdr msg = {0};
  char m_buffer[256], c_buffer[256];
  struct iovec io = { .iov_base = m_buffer, .iov_len = sizeof(m_buffer) };

  msg.msg_iov = &io;
  msg.msg_iovlen = 1;

  msg.msg_control = c_buffer;
  msg.msg_controllen = sizeof(c_buffer);

  if (recvmsg(socket, &msg, 0) < 0) {
    printf("Failed to receive message\n");
    return -1;
  }

  struct cmsghdr * cmsg = CMSG_FIRSTHDR(&msg);
  unsigned char * data = CMSG_DATA(cmsg);
  int fd = *((int*) data);

  return fd;
}


int bind_server() {
  int sock;
  struct sockaddr_in addr;

  sock = socket(AF_INET, SOCK_STREAM, 0);
  if(sock == -1) {
    printf("invalid socket.");
    return sock;
  }

  memset(&addr, 0, sizeof(struct sockaddr_in));

  addr.sin_family = AF_INET;
  addr.sin_port = 0;

  inet_pton(AF_INET, "127.0.0.1", &addr.sin_addr);
  
  bind(sock, (struct sockaddr *)&addr, sizeof(addr));
  listen(sock, 5);

  return sock;
}



int main(int argc, char * argv[]) {

  int sv[2], pid;
  if (socketpair(AF_UNIX, SOCK_DGRAM, 0, sv) != 0) {
    printf("Failed to create Unix-domain socket pair\n");
    return -1;
  }

  pid = fork();
  if (pid > 0) {
    int sock = sv[0];
    int fd;
    char cmd[256];

    close(sv[1]);

    fd = bind_server();
    printf("binded server socket fd %d.\n", fd);

    sprintf(cmd, "stat /proc/%d/fd/%d", pid, fd);
    system(cmd);

    send_fd(sock, fd);

    close(fd);
    waitpid(pid, NULL, 0);

  }
  else {
    int sock = sv[1];
    char cmd[256];
    int fd;

    close(sv[0]);
    nanosleep(&(struct timespec){ .tv_sec = 0, .tv_nsec = 500000000}, 0);

    fd = recv_fd(sock);
    printf("Received fd %d!\n", fd);

    pid = getpid();

    sprintf(cmd, "stat /proc/%d/fd/%d", pid, fd);
    system(cmd);

    close(fd);
  }

  return 0;

}
