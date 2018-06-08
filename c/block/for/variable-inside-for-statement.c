
#include "stdio.h"


int main(int argc, char * argv[]) {
  int i = 0;
  for(; i < 10; i++) {
    int j = i;
    printf("Variable j's address 0x%lx.\n", (unsigned long)&j);
  }

  return 0;
}
