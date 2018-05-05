
#include "stdio.h"
#include <stdlib.h>


int main(int argc, char * argv[]){

  int num;
  if(argc == 1) num = 0;
  else num = atoi(argv[1]);

  char *out_str;

  switch(num) {

  case 0:
    out_str = "zero";
    break;

  case 1:
    out_str = "one";
    break;

  case 2:
    out_str = "two";
    break;

  default:
    out_str = "unknow";

  }

  printf("%d's string is %s.\n", num, out_str);

  return 0;

}
