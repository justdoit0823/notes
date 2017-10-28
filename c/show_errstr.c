
#include "stdio.h"
#include "string.h"


int main(int argc, char * argv[])
{
  int err_no = atoi(argv[1]);
  printf("error number %d's error string is %s.\n", err_no, strerror(err_no));
  return 0;
}
