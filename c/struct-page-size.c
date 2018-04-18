
#include "stdlib.h"
#include "linux/mm_types.h"


int main(int argc, char * argv[]){
  printf("struct page's size is %d.\n", sizeof(struct page));
  return 0;
}
