
#include <Python.h>
#include "stdio.h"


PyTypeObject * create_type(const char * name){
  PyObject * args, * dict, * value;
  PyTypeObject * new_type;

  args = PyTuple_New(3);
  PyTuple_SetItem(args, 0, PyUnicode_FromString(name));
  PyTuple_SetItem(args, 1, PyTuple_New(0));

  dict = PyDict_New();
  value = PyUnicode_FromString("haha");
  PyDict_SetItem(dict, PyUnicode_FromString("__get__"), value);
  PyTuple_SetItem(args, 2, dict);

  new_type = (PyTypeObject *)PyType_Type.tp_new(&PyType_Type, args, NULL);

  return new_type;
}


int main(int argc, char * argv[]){
  PyTypeObject * new_type, * new_type1;
  Py_Initialize();

  new_type = create_type("MyType");
  new_type1 = create_type("MyType1");

  printf("new type name %s, %lx.\n", new_type->tp_name, (unsigned long)new_type->tp_descr_get);
  printf("new type name %s, %lx.\n", new_type1->tp_name, (unsigned long)new_type1->tp_descr_get);

  printf("type type name %s, %lx.\n", PyType_Type.tp_name, (unsigned long)PyType_Type.tp_descr_get);

  return 0;
}
