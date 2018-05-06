
#include "Python.h"

#include "stdio.h"
#include "stdlib.h"


int main(int argc, char * argv[]){

  PyTypeObject all_types[] = {
    PyLong_Type, PyFloat_Type, PySet_Type, PySlice_Type, PyTuple_Type,
    PyList_Type, PyDict_Type};

  Py_Initialize();

  PyTypeObject b_type;
  for(int i=0; i < sizeof(all_types) / sizeof(PyTypeObject); i++) {
    b_type = all_types[i];
    printf("%s dictoffset %zd, item size %zd.\n", b_type.tp_name, b_type.tp_dictoffset, b_type.tp_itemsize);

    if(b_type.tp_dict == NULL) PyType_Ready(&b_type);

    printf("After type ready: ");
    printf("%s dictoffset %zd, item size %zd.\n", b_type.tp_name, b_type.tp_dictoffset, b_type.tp_itemsize);
  }

  if (Py_FinalizeEx() < 0) {
    exit(120);
  }

  return 0;

}
