
#include "stdio.h"
#include <stdlib.h>
#include "pthread.h"


typedef struct cache_aligned {

  unsigned long cnt_a;
  char cnt_padding[56];
  unsigned int cnt_b;

} c_aligned_t;


typedef struct cache_unaligned {

  unsigned long cnt_a;
  unsigned int cnt_b;

} c_unaligned_t;


typedef struct thread_param {

  void * ptr;
  unsigned long num;
  unsigned int field;

} t_param;


typedef void * (* foo_thread_func) (void *);


void * aligned_foo(void * args){
  t_param * t_args = (t_param *)args;
  c_aligned_t * ptr = (c_aligned_t *)t_args->ptr;

  unsigned long num = t_args->num;
  unsigned int field = t_args->field;
  unsigned long sum = 0;

  printf("num %lu, field %d.\n", num, field);

  if (field == 1) while(--num > 0) ptr->cnt_a += 1;
  else while(num-- > 0) sum += ptr->cnt_b;

  printf("finish field %d.\n", field);
  return NULL;
}


void * unaligned_foo(void * args){
  t_param * t_args = (t_param *)args;
  c_unaligned_t * ptr = (c_unaligned_t *)t_args->ptr;

  unsigned long num = t_args->num;
  unsigned int field = t_args->field;
  unsigned long sum = 0;

  printf("num %lu, field %d.\n", num, field);

  if (field == 1) while(--num > 0) ptr->cnt_a += 1;
  else while(num-- > 0) sum += ptr->cnt_b;

  printf("finish field %d.\n", field);
  return NULL;
}


int main(int argc, char * argv[]){
  foo_thread_func thread_routine;
  pthread_t threads[2];
  t_param params[2];

  unsigned long num = 100000, aligned = 0;
  int t_ret, j_ret;

  if(argc < 2){
    printf("operation num is missing.\n");
    return 0;
  }
  num = atol(argv[1]);

  if(argc > 2) aligned = atoi(argv[2]);
  printf("num %ld, aligned %ld.\n", num, aligned);

  if(aligned){
    c_aligned_t a_data;

    a_data.cnt_a = 0;
    a_data.cnt_b = 1;

    for (int i = 0; i < 2; i++) {
      params[i].ptr = &a_data;
      params[i].num = num;
      params[i].field = i + 1;
    }

    thread_routine = aligned_foo;

    printf("runing aligned cace line test.\n");
  }
  else{
    c_unaligned_t u_data;

    u_data.cnt_a = 0;
    u_data.cnt_b = 1;

    for (int i = 0; i < 2; i++) {
      params[i].ptr = &u_data;
      params[i].num = num;
      params[i].field = i + 1;
    } 

    thread_routine = unaligned_foo;

    printf("runing unaligned cace line test.\n");
  }

  for(int i = 0; i < 2; i++) {
    t_ret = pthread_create(&threads[i], NULL, thread_routine, &params[i]);
    if(t_ret != 0){
      printf("create thread failed.\n");
      return 0;
    }
  }

  void * ret;
  for(int i = 0; i < 2; i++) {
    j_ret = pthread_join(threads[i], &ret);
    if(j_ret != 0) printf("create thread failed.\n");
  }

  printf("test done.\n");
  return 0;
}
