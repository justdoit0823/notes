
#include "Python.h"

#include "stdio.h"
#include "stdlib.h"


int main(int argc, char * argv[]){

  Py_Initialize();

  if(PyType_Type.tp_dict == NULL) PyType_Ready(&PyType_Type);

  printf("type's alloc %s PyType_GenericAlloc and %s to object's alloc.\n", PyType_Type.tp_alloc == PyType_GenericAlloc ? "is" : "isn't", PyType_Type.tp_alloc == PyBaseObject_Type.tp_alloc ? "equals" : "doesn't equal");
  printf("object's basic size is %lu, type's basic size is %zd, PyHeapTypeObject's size is %lu.\n", PyBaseObject_Type.tp_basicsize, PyType_Type.tp_basicsize, sizeof(PyHeapTypeObject));

  if (Py_FinalizeEx() < 0) {
    exit(120);
  }

  return 0;

}
