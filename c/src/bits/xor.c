
#include "stdio.h"
#include <stdlib.h>


int main(int argc, char * argv[]){

  if(argc < 3){
    printf("Two operands are needed.");
    return 0;
  }

  int left_operand, right_operand;

  left_operand = atoi(argv[1]);
  right_operand = atoi(argv[2]);

  printf("%d ^ %d result is %d.\n", left_operand, right_operand, left_operand ^ right_operand);
  return 0;

}
