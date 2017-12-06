
#include "stdio.h"
#include <stdlib.h>
#include "pthread.h"


typedef struct cache_aligned {

  unsigned long cnt_a;
  unsigned long cnt_b;

} c_aligned_t;


typedef struct cache_unaligned {

  unsigned long cnt_a;
  unsigned long cnt_b;

} c_unaligned_t;


typedef struct thread_param {

  void * ptr;
  unsigned long num;
  unsigned int field;

} t_param;


typedef void (* foo_thread_func) (void *);


void * aligned_foo(void * args){
  t_param * t_args = (t_param *)args;
  c_aligned_t * ptr = (c_aligned_t *)t_args->ptr;
  unsigned long num = t_args->num;
  unsigned int field = t_args->field;

  if (field == 1) while(num-- > 0) ptr->cnt_a += num * 2;
  else while(num-- > 0) ptr->cnt_b += num * 2;

  return NULL;

}


void * unaligned_foo(void * args){
  t_param * t_args = (t_param *)args;
  c_unaligned_t * ptr = (c_unaligned_t *)t_args->ptr;
  unsigned long num = t_args->num;
  unsigned int field = t_args->field;

  if (field == 1) while(num-- > 0) ptr->cnt_a += num * 2;
  else while(num-- > 0) ptr->cnt_b += num * 2;

  return NULL;

}


int main(int argc, char * argv[]){

  pthread_t tid1, tid2;
  t_param param1, param2;
  unsigned long num = 0xffffffff - 1;
  unsigned int aligned = 0;
  if(argc > 1) aligned = atoi(argv[1]);

  if(aligned){
    c_aligned_t c_data1, c_data2;
    c_data1.cnt_a = 0;
    c_data1.cnt_b = 0;

    c_data2.cnt_a = 0;
    c_data2.cnt_b = 0;

    param1.ptr = &c_data1;
    param1.num = num;
    param1.field = 1;

    param2.ptr = &c_data2;
    param2.num = num;
    param2.field = 2;

    pthread_create(&tid1, NULL, aligned_foo, &param1);
    pthread_create(&tid2, NULL, aligned_foo, &param2);

    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
  }
  else{
    c_unaligned_t c_data1, c_data2;
    c_data1.cnt_a = 0;
    c_data1.cnt_b = 0;

    c_data2.cnt_a = 0;
    c_data2.cnt_b = 0;

    param1.ptr = &c_data1;
    param1.num = num;
    param1.field = 1;

    param2.ptr = &c_data2;
    param2.num = num;
    param2.field = 2;

    pthread_create(&tid1, NULL, unaligned_foo, &param1);
    pthread_create(&tid2, NULL, unaligned_foo, &param2);

    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
  }

  return 0;

}
