
#include "unistd.h"
#include "stdio.h"
#include "stdlib.h"
#include <sys/time.h>


void foo(int num){
  int sum;
  sum = 0;
  while(num-- > 0) sum += num;
}


int main(int argc, char * argv[]){
  struct timeval s_time, e_time;
  int num, duration;

  if(argc > 1) num = atoi(argv[1]);
  else num = 1000;

  gettimeofday(&s_time, NULL);
  foo(num);
  gettimeofday(&e_time, NULL);

  duration = (e_time.tv_sec - s_time.tv_sec) * 1000000 + e_time.tv_usec - s_time.tv_usec;

  printf("foo with num %d runs %d microseconds.\n", num,  duration);
  return 0;
}
