
#include "pthread.h"
#include "unistd.h"
#include "stdio.h"


void show_process_info(const char * process_name){
  pid_t pid;
  pthread_t cur_thread;
  cur_thread = pthread_self();
  pid = getpid();
  printf("%s run in thread %ld, process %d.\n", process_name, (long)cur_thread, pid);
}


void * thread_handler(void * ptr_val){
  show_process_info("my new thread");
  return NULL;
}


int main(int argc, char * argv[]){
  show_process_info("main tread");
  pthread_t m_thead;
  if(pthread_create(&m_thead, NULL, thread_handler, NULL) != 0){
    printf("create thread failed.\n");
    return -1;
  }

  pthread_join(m_thead, NULL);
  return 0;
}
