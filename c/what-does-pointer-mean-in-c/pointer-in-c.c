
#include "stdio.h"


typedef void (* p_void_func) (void);


void foo(void){

  printf("invoke foo function.\n");

}


int main(int argc, char * argv[]){
  int i;
  int * p_i, ** p__i;
  p_void_func p_func;

  p_i = &i;
  p__i = &p_i;

  printf("variable's address, 0x%x, 0x%x, 0x%x.\n", (unsigned int)&i, (unsigned int)&p_i, (unsigned int)&p__i);

  p_func = foo;
  (*p_func)();

  return 0;
}
