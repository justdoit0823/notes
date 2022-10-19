
#include "stdio.h"
#include "stdlib.h"
#include "pthread.h"


typedef struct {
  int idx;
  long start;
  long stop;
  long long * r;
} TaskArg;


void sum_task(void * arg){
  TaskArg * p = (TaskArg *)arg;
  long n_start, n_stop;
  long long total = 0;
  n_start = p->start;
  n_stop = p->stop;

  while(n_start < n_stop){
    total += n_start;
    n_start += 1;
  }

  (p->r)[p->idx] = total;
}


int main(int argc, char * argv[]){
  long num, thread_num, size;
  long long total = 0, * ret;
  pthread_t * threads;
  TaskArg * args;

  num = atoi(argv[1]);
  thread_num = atoi(argv[2]);
  size = (long)(num / thread_num);

  ret = (long long *)malloc(sizeof(long long) * thread_num);
  if(ret == NULL) {
    printf("Invalid pointer.\n");
    return -1;
  }

  threads = (pthread_t *)malloc(sizeof(pthread_t) * thread_num);
  if(threads == NULL) {
    printf("allocate memory failed.\n");
    return -1;
  }

  args = (TaskArg *)malloc(sizeof(TaskArg) * thread_num);
  if(args == NULL) {
    printf("Allocate memory failed.\n");
    return -1;
  }

  for(int i=0; i < thread_num; i++) {
    args[i].idx = i;
    args[i].start = i * size;
    if(i == thread_num - 1) args[i].stop = num;
    else args[i].stop = (i + 1) * size;
    args[i].r = ret;

    if(pthread_create(&threads[i], NULL, sum_task, &args[i]) !=0 ){
      printf("start thread failed.\n");
      break;
    }
  }

  for(int i=0; i < thread_num; i++) {
    pthread_join(threads[i], NULL);
    total += ret[i];
  }

  printf("sum %lld.\n", total);

  return 0;
}