
#include "stdlib.h"
#include "stdio.h"
#include "sys/time.h"
#include "unistd.h"
#include "pthread.h"


typedef struct {
	unsigned int capacity;
	unsigned int size;
	unsigned int last_index;
	int * data;
} List;


List * new_list(unsigned int cap) {
	if(cap <= 0) return NULL;

	int * p;
	List * list;
	p = malloc(sizeof(int) * cap);
	if(p == NULL) return NULL;

	list = malloc(sizeof(List));
	if(list == NULL) {
		free(p);
		return NULL;
	}

	list->capacity = cap;
	list->size = 0;
	list->last_index = 0;
	list->data = p;

	return list;
}


int append_list(List * p, int item) {
	if(p->size == p->capacity) return 0;

	p->data[p->last_index++] = item;
	p->size++;

	return 1;
}


void traverse_list(List * p) {
	printf("[");
	for(int i=0; i < p->size; i++) {
		if(i > 0) printf(",%d", p->data[i]);
		else printf("%d", p->data[i]);
	}
	printf("]");
}


void free_list(List * p) {
	free(p->data);
	free(p);
}


typedef struct {
	int seq;
	List * p;
	pthread_mutex_t * l;
	pthread_mutex_t * cl;
	pthread_cond_t * c;
	int * f;
} TaskArg;


void * fill_list(void * arg) {
	TaskArg * t = (TaskArg *)arg;
	List * p = t->p;
	int seq = t->seq;

	pthread_mutex_lock(t->cl);
	while(!t->f) pthread_cond_wait(t->c, t->cl);
	pthread_mutex_unlock(t->cl);

	struct timeval tv;
	gettimeofday(&tv, NULL);
	printf("thread %d %ld.%06ld.\n", seq, tv.tv_sec, tv.tv_usec);

	for(int i = 0; i < 10; i++) {
		pthread_mutex_lock(t->l);
		append_list(p, seq * 100 + i);
		pthread_mutex_unlock(t->l);
	}

	return NULL;
}


int main(int argc, char * argv[]) {

	int started = 0;
	TaskArg args[5];

	pthread_t threads[5];
	pthread_mutex_t lock, c_lock;
	pthread_cond_t start_cond;

	pthread_mutex_init(&lock, NULL);
	pthread_mutex_init(&c_lock, NULL);
	pthread_cond_init(&start_cond, NULL);

	List * p = new_list(50);

	for(int i = 0; i < 5; i++) {
		args[i].seq = i;
		args[i].p = p;
		args[i].l = &lock;
		args[i].cl = &c_lock;
		args[i].c = &start_cond;
		args[i].f = &started;
		pthread_create(&threads[i], NULL, fill_list, &args[i]);
	}

	started = 1;
	pthread_cond_broadcast(&start_cond);
	for(int i = 0; i < 5; i++) pthread_join(threads[i], NULL);

	pthread_mutex_destroy(&lock);
	pthread_mutex_destroy(&c_lock);
	pthread_cond_destroy(&start_cond);

	traverse_list(p);
	free_list(p);

	printf("\n");

	return 0;
}
