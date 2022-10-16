#include "stdio.h"
#include "time.h"
#include "unistd.h"
#include "pthread.h"
#include "signal.h"

typedef void (*sighandler_t)(int);


static sighandler_t oldsh;


/* unsigned int sleep(unsigned int seconds) */
/* { */
/*   int ret; */
/*   ret = alarm(seconds); */
/*   pause(); */
/*   return ret; */
/* } */


void * test_sleep_5(void * pdata)
{
  time_t t1, t2;
  struct timespec ts;
  ts.tv_sec = 5;
  ts.tv_nsec = 0;
  printf("start thread test_sleep_5 at %lf...\n", (double)time(&t1));
  sleep(5);
  /* nanosleep(&ts, NULL); */
  printf("stop thread test_sleep_5 at %lf...\n", (double)time(&t2));
  return NULL;
}


void * test_sleep_8(void * pdata)
{
  time_t t1, t2;
  struct timespec ts;
  printf("start thread test_sleep_8 at %lf...\n", (double)time(&t1));
  /* sleep(8); */
  nanosleep(&ts, NULL);
  printf("stop thread test_sleep_8 at %lf...\n", (double)time(&t2));
  return NULL;
}


void sig_alarm_hook(int sig)
{
  printf("recv signal %d at %lf...\n", sig, (double)time(NULL));
  oldsh(sig);
}



int main(int argc, char * argv[])
{
  pthread_t pt1, pt2;

  /* if((oldsh=signal(SIGALRM, (sighandler_t)sig_alarm_hook)) == SIG_ERR){ */
  /*   printf("change SIGALRM handler error...\n"); */
  /*   return -1; */
  /* } */

  /* pthread_create(&pt1, NULL, test_sleep_5, NULL); */
  /* /\* printf("start thread pt1 at %p...\n", (unsigned int *)pt1); *\/ */
  /* pthread_create(&pt2, NULL, test_sleep_8, NULL); */
  /* /\* printf("start thread pt2 at %p...\n", (unsigned int *)pt2); *\/ */

  /* /\* alarm(1); *\/ */

  /* pthread_join(pt1, NULL); */
  /* pthread_join(pt2, NULL); */
  test_sleep_5(NULL);

  return 0;
}
