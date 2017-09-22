
#include "stdio.h"


int hello(const char * str){
  printf("%s.\n", str);
  return 0;
}


int main(int argc, char * argv[]){
  hello(argv[0]);
  return 0;
}
