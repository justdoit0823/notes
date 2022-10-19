#include "Python.h"
//#include "stdio.h"

//extern PyTypeObject PyType_Type;
//PyAPI_DATA(PyTypeObject) PyType_Type; /* built-in 'type' */

int main(int argc, char * argv[]){
  int i = 0;
  Py_Initialize();
  PyTypeObject * pptype = &PyType_Type;
  printf("orign type %s desc %lx, %lx.\n", pptype->tp_doc, (unsigned long)(pptype), (unsigned long)&pptype->tp_descr_get);
  PyTypeObject ptype, btype = PyType_Type, PyBaseObject_Type;
  printf("i 0x%lx, %lx, %lx.\n", (unsigned long)&i, (unsigned long)pptype->tp_descr_get, (unsigned long)ptype.tp_descr_get);
  printf("type name %s, %lx, %lx.\n", PyType_Type.tp_name, (unsigned long)&ptype.tp_descr_get, (unsigned long)&ptype);
  printf("type 0x%lx, descr get %lx.\n", (unsigned long)&PyType_Type, (unsigned long)PyType_Type.tp_descr_get);
  printf("object descr get %lx.\n", (unsigned long)PyBaseObject_Type.tp_descr_get);
  /* PyType_Ready(&PyBaseObject_Type); */
  /* PyType_Ready(&PyType_Type); */
  /* PyType_Ready(&ptype); */
  /* printf("descr get %lx.\n", (unsigned long)ptype.tp_descr_get); */
  printf("type descr get %x.\n", (unsigned int)PyType_Type.tp_descr_get);
  printf("object descr get %x.\n", (unsigned int)PyBaseObject_Type.tp_descr_get);
  return 0;
}