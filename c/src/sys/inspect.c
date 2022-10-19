#include <stdio.h>
#include <stdlib.h>
#include <sys/uio.h>

#include <Python.h>
#include <dlfcn.h>


int main(int argc, char * argv[]) {
  if (argc < 2) {
    printf("pid is needed.\n");
    return 0;
  }

  int pid = atoi(argv[1]);

  struct iovec local[1], remote[1];
  int size=100;
  char buf[100];

  local[0].iov_base = buf;
  local[0].iov_len = size;
  remote[0].iov_base = (void *) 0x0000000000000040;
  remote[0].iov_len = size;

  int nread = process_vm_readv(pid, local, 1, remote, 1, 0);
  printf("read %d bytes.\n", nread);

  printf("inited %s.\n", ((int *)buf)[0]);

  return 0;
}