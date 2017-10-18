
#include <math.h>
#include "stdlib.h"
#include <stdio.h>


int sum(int count){
  long sum = 0;
  int i;
  while(count--){
    for(i = 0; i < sqrt(sum); i++) {}
    sum += count / (sum + 1);
  }
  return sum;
}


int main(int argc, char * argv[]){
  int count = 10000;
  long total = 0;
  if(argc > 1) count = atoi(argv[1]);

  total = sum(count);
  printf("total is %ld.\n", total);
  return 0;
}
