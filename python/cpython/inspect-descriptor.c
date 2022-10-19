#include <Python.h>
#include "stdio.h"


PyObject * descr_get(PyObject * descr, PyObject * obj, PyObject * type){
  return Py_True;
}


int main(int argc, char * argv[]){
  PyObject * args, * kwargs, * value;
  PyTypeObject * new_type;
  Py_Initialize();
  args = PyTuple_New(3);
  printf("tuple %lx.\n", (unsigned long)args);
  PyTuple_SetItem(args, 0, PyUnicode_FromString("MyType"));
  PyTuple_SetItem(args, 1, PyTuple_New(0));
  printf("tuple %lx.\n", (unsigned long)args);
  kwargs = PyDict_New();
  value = PyUnicode_FromString("haha");
  PyDict_SetItem(kwargs, PyUnicode_FromString("__get__"), value);
  PyTuple_SetItem(args, 2, kwargs);
  printf("tuple size %d.\n", PyTuple_GET_SIZE(args));
  new_type = (PyTypeObject *)PyType_Type.tp_new(&PyType_Type, args, NULL);
  printf("new type name %s, %lx, %lx\n", new_type->tp_name, (unsigned long)new_type->tp_descr_get, (unsigned long)value);
  return 0;
}