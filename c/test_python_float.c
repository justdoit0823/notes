#include "Python.h"
#include "stdio.h"
#include "pystrtod.h"


int main(int argc, char * argv[])
{
  double d = 100.1;
  printf("double value is %.17g, %s\n", d, PyOS_double_to_string(d, 'r', 0, Py_DTSF_ADD_DOT_0, NULL));
  return 0;
}
