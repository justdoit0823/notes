
// A simple jit program, read more detail at http://blog.reverberate.org/2012/12/hello-jit-world-joy-of-simple-jits.html


#include "stdio.h"
#include "stdlib.h"
#include <string.h>

#include <sys/mman.h>


/*
  We can define a complete add function as the following,

  int add(int a, int b){
    return a + b;
  }

  Then compile this function to an object file.
  `gcc -c add_function.c`

  Next, we can use `objdump` to get the machine code.

  `objdump -disassemble add_function.o`

*/


static unsigned char code[] = {
  0x55, 0x48, 0x89, 0xe5, 0x89, 0x7d, 0xfc, 0x89, 0x75, 0xf8, 0x8b, 0x75, 0xfc,
  0x03, 0x75, 0xf8, 0x89, 0xf0, 0x5d, 0xc3
};


typedef int (*int_add) (int, int);


int main(int argc, char * argv[]){
  int a, b, ret;
  char * mem_addr;
  int_add func_addr;

  if(argc < 3){
    printf("two operands are need.\n");
    return -1;
  }

  a = atoi(argv[1]);
  b = atoi(argv[2]);

  mem_addr = mmap(NULL, sizeof(code), PROT_WRITE|PROT_EXEC, MAP_ANON|MAP_PRIVATE, -1, 0);
  if(mem_addr == NULL){
    printf("map memory failed.\n");
    return -1;
  }
  memcpy(mem_addr, code, sizeof(code));

  func_addr = (int_add)mem_addr;
  printf("func result %d\n", func_addr(a, b));

  if(munmap(mem_addr, sizeof(code)) == -1){
    printf("unmap memory failed.\n");
  }

  return 0;
}
