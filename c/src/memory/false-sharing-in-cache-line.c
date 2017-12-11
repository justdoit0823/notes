
#include "stdio.h"
#include <stdlib.h>
#include "pthread.h"


typedef struct cache_aligned {

  unsigned long cnt_a;
  unsigned long cnt_b;

} c_aligned_t;


typedef struct cache_unaligned {

  unsigned int cnt_a;
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

  pthread_t tid1, tid2;
  foo_thread_func thread_routine;
  t_param param1, param2;
  unsigned long num, aligned = 0;
  int t_ret, j_ret;
  c_aligned_t a_data;
  c_unaligned_t u_data;

  if(argc < 2){
    printf("operation num is missing.\n");
    return 0;
  }
  num = atol(argv[1]);
  if(argc > 2) aligned = atoi(argv[2]);
  printf("num %ld, aligned %ld.\n", num, aligned);

  printf("unsigned long size is %ld, and unsigned int size is %ld.\n", sizeof(unsigned long), sizeof(unsigned int));

  if(aligned){
    a_data.cnt_a = 0;
    a_data.cnt_b = 1;

    param1.ptr = &a_data;
    param1.num = num;
    param1.field = 1;

    param2.ptr = &a_data;
    param2.num = num;
    param2.field = 2;

    thread_routine = aligned_foo;
    printf("runing aligned cace line test.\n");
  }
  else{
    u_data.cnt_a = 0;
    u_data.cnt_b = 1;

    param1.ptr = &u_data;
    param1.num = num;
    param1.field = 1;

    param2.ptr = &u_data;
    param2.num = num;
    param2.field = 2;

    thread_routine = unaligned_foo;
    printf("runing unaligned cace line test.\n");
  }

  t_ret = pthread_create(&tid1, NULL, thread_routine, &param1);
  if(t_ret != 0){
    printf("create thread failed.\n");
    return 0;
  }
  t_ret = pthread_create(&tid2, NULL, thread_routine, &param2);
  if(t_ret != 0){
    printf("create thread failed.\n");
    return 0;
  }

  void * ret;

  j_ret = pthread_join(tid1, &ret);
  if(j_ret != 0) printf("create thread failed.\n");
  j_ret = pthread_join(tid2, &ret);
  if(j_ret != 0) printf("create thread failed.\n");

  printf("finish test.\n");

  return 0;

}
