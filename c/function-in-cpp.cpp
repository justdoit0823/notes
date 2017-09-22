
#include "stdio.h"


class MyClass {

private:
  int x;

public:

  void hello(){
    printf("hello.\n");
  }

};


int main(int argc, char * argv[]){
  MyClass * obj = NULL;
  obj->hello();
  return 0;
}
