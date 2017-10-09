
#include "stdio.h"
#include "stdlib.h"
#include "unistd.h"
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>


static long test_size = (long)10 * 1024 * 1024 * 1024;


int main(int argc, char * argv[]){
  int pagesize, fd, sync, last_sync, flags;
  long write_bytes;
  char * temp_buf, *file_path, path_temp[] = "/tmp/disk-io-XXXXXX";
  if(argc < 2){
    printf("pagesize is needed.\n");
    return 0;
  }
  pagesize = atoi(argv[1]);
  sync = 0;
  last_sync = 0;
  if(argc > 2) sync = atoi(argv[2]);
  if(argc > 3) last_sync = atoi(argv[3]);

  flags = O_CREAT|O_WRONLY;
  if(sync) flags |= O_SYNC;
  temp_buf = malloc(pagesize);
  memset(temp_buf, 48, pagesize);

  file_path = mktemp(path_temp);
  if(file_path == NULL){
    printf("create temp path failed.\n");
    return 0;
  }
  fd = open(file_path, flags, 0644);
  if(fd == -1){
    printf("open file failed %s.\n", strerror(errno));
    return 0;
  }

  write_bytes = 0;
  printf("write to temp file %s .\n", file_path);
  for(int i=0; i < test_size / pagesize; i++){
    write_bytes += write(fd, temp_buf, pagesize);
  }
  if(last_sync) fsync(fd);

  printf("successfully write %ld bytes.\n", write_bytes);
  return 0;
}
