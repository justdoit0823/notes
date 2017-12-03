
#include "stdio.h"

typedef int (*foo_ptr) (void);


int hello(const char * str){
  printf("hello %s.\n", str);
  return 0;
}


int foo(void){
  printf("foo function.\n");
  return 0;
}


int main(int argc, char * argv[]){
  foo_ptr f_ptr = foo;
  hello(argv[0]);
  (*f_ptr)();
  return 0;
}
