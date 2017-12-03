
#include "stdio.h"


int main(int argc, char * argv[]){

  unsigned int check_a = 1;

  if(*(unsigned char *)&check_a == 1) printf("Little endian machine.\n");
  else printf("Little endian machine.\n");

  return 0;

}
