
#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include <sys/utsname.h>

typedef void (*func) (void);


void darwin_show_sys(){
  printf("show darwin system info.\n");
}


void linux_show_sys(){
  printf("show linux system info.\n");
}


int main(int argc, char * argv[]){
  func test_func;
  struct utsname sys_name;
  uname(&sys_name);
  if(strcmp(sys_name.sysname, "Darwin") == 0) test_func = darwin_show_sys;
  else test_func = linux_show_sys;

  test_func();

  return 0;
}
