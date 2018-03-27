
#include "stdio.h"
#include <sys/time.h>
#include "unistd.h"

void call_gettimeofday(void){

  struct timeval tv;
  struct timezone tz;

  for(int i=0; i < 100; i++){
    gettimeofday(&tv, &tz);
    int tz_hour = (0 - tz.tz_minuteswest) / 60;
    printf("time of day is %ld.%d with timezone %d:%d\n", tv.tv_sec, tv.tv_usec, tz_hour, tz.tz_dsttime);
  }

}


int main(int argc, char * argv[]){

  call_gettimeofday();
  return 0;

}
