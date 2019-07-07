
#include <stdio.h>

#include <Python.h>
#include <dlfcn.h>

#include <pthread.h>


void * worker_task(void * arg) {
  PyRun_SimpleString("import time\nprint(f'current ts in {time.time()} in non main thread.')");
  return NULL;
}


int main(int argc, char * argv[]) {
  Py_Initialize();

  const char * path = "/usr/local/opt/python/Frameworks/Python.framework/Versions/3.7/lib/python3.7/config-3.7m-darwin/libpython3.7.a";
  void * handle = dlopen(path, RTLD_LAZY | RTLD_GLOBAL);
  if (handle == NULL) {
    printf("load failed.\n");
    return 1;
  }

  PyObject * (* f_dict_new) ();
  int (* f_dict_set)(PyObject *, PyObject *, PyObject *);

  PyObject * (* f_import)(PyObject *);
  PyObject * (* f_getattr)(PyObject *, const char *);
  PyObject * (* f_call)(PyObject *, ...);

  PyObject * (* f_from_string)(const char *);
  double (* f_to_float)(PyObject *);

  f_dict_new = dlsym(handle, "PyDict_New");
  f_dict_set = dlsym(handle, "PyDict_SetItem");

  f_import = dlsym(handle, "PyImport_Import");
  f_getattr = dlsym(handle, "PyObject_GetAttrString");
  f_call = dlsym(handle, "PyObject_CallFunctionObjArgs");

  f_from_string = dlsym(handle, "PyUnicode_FromString");
  f_to_float = dlsym(handle, "PyFloat_AsDouble");

  PyObject * d = (*f_dict_new)();
  PyObject * s1 = (*f_from_string)("foo");
  PyObject * s2 = (*f_from_string)("bar");

  (*f_dict_set)(d, s1, s2);

  const char * (*f_to_utf8)(PyObject *);

  PyObject * m_builtin = (*f_import)((*f_from_string)("builtins"));
  PyObject * f_str = (*f_getattr)(m_builtin, "str");
  f_to_utf8 = dlsym(handle, "PyUnicode_AsUTF8");
  PyObject * d_content = (*f_call)(f_str, d, NULL);
  printf("dict d's value %s.\n", (*f_to_utf8)(d_content));

  PyObject * m_time = (*f_import)((*f_from_string)("time"));
  PyObject * f_time = (*f_getattr)(m_time, "time");
  PyObject * ts1 = (*f_call)(f_time, NULL);

  double ts2 = (*f_to_float)(ts1);
  printf("current ts %lf in main thread.\n", ts2);

  pthread_t task;
  pthread_create(&task, NULL, worker_task, NULL);

  if (Py_FinalizeEx() < 0) {
    exit(120);
  }

  return 0;
}
