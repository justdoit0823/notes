
#include "stdio.h"
#include <spawn.h>
#include "unistd.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>


int main(int argc, char * argv[]){
  char * cmd = argv[1];
  pid_t cur_pid;
  cur_pid = getpid();
  printf("current process %d.\n", cur_pid);
  if(strcmp(cmd, "file") == 0){
    test_file_fd(argv[2], argv[3]);
  }
  else if(strcmp(cmd, "env") == 0){
    test_environment();
  }

  return 0;
}


int test_file_fd(char * timeout, char * path){
  pid_t child_pid;
  int ret;
  char * spawn_args[] = {"/bin/sleep", timeout, NULL};
  int fd1 = open("/etc/hosts", O_RDONLY);
  int fd2 = open(path, O_RDWR);
  dup2(fd2, 2);
  close(fd1);
  ret = posix_spawn(&child_pid, "/bin/sleep", NULL, NULL, spawn_args, NULL);
  if(ret != 0){
    printf("spawn failed.\n");
    return 0;
  }
  printf("new child process %d.\n", child_pid);
  sleep(atoi(timeout));
}


int test_environment(){
  pid_t child_pid;
  int ret;
  char * spawn_args[] = {"/usr/bin/printenv", NULL};
  char * test_spawn = getenv("TEST_SPAWN");
  printf("TEST_SPWAN environment %s.\n", test_spawn);
  ret = posix_spawn(&child_pid, "/usr/bin/printenv", NULL, NULL, spawn_args, NULL);
  if(ret != 0){
    printf("spawn failed.\n");
    return 0;
  }
  printf("new child process %d.\n", child_pid);
}
