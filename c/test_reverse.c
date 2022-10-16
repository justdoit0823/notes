#include "stdio.h"


struct NodeType{
  int d;
  struct NodeType * next;
};

typedef struct NodeType Node;

void reverse(Node * head){
  Node * prev, * cur, * next;
  prev = NULL;
  cur = head;

  while(cur){
    next = cur->next;
    cur->next = prev;
    prev = cur;
    cur = next;
  }
}

int main(int argc, char * argv[]){
  Node a, b, c;
  a.d = 123;
  a.next = &b;

  b.d = 12;
  b.next = &c;

  c.d = 1231;
  c.next = NULL;

  reverse(&a);

  Node * p = &c;
  printf("Node value is : ");

  while(p != NULL){
    printf("%d ", p->d);
    p = p->next;
  }
  
  return 0;
}
