
What Is Embedding
==================

Embedding Python is similar to extending it, but not quite. The difference is that when you extend Python, the main program of the application is still the Python interpreter,

while if you embed Python, the main program may have nothing to do with Python — instead, some parts of the application occasionally call the Python interpreter to run some Python code.


Embedding Process
=================

Initialize
----------

If you are embedding Python, you are providing your own main program. One of the things this main program has to do is initialize the Python interpreter.

At the very least, you have to call the function Py_Initialize(). There are optional calls to pass command line arguments to Python. Then later you can call the interpreter from any part of the application.


Call Interpreter
----------------

There are several different ways to call the interpreter: you can pass a string containing Python statements to PyRun\_SimpleString(), or you can pass a stdio file pointer and a file name (for identification in error messages only) to PyRun_SimpleFile().

You can also call the lower-level operations to construct and use Python objects.


Write A Simple Example
========================

*This example is using Python 3 style.*

C Source Code
-------------

A simple c source file named embedding_example.c like the fllowing:

```
#include <Python.h>
#include "stdio.h"

int
main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    Py_SetProgramName(program);  /* optional but recommended */
    Py_Initialize();
    printf("Python version %s.\n", Py_GetVersion());
    PyRun_SimpleString("from time import time,ctime\n"
                       "print('Today is', ctime(time()))\n");
    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    PyMem_RawFree(program);
    return 0;
}
```

There may be some differences between Python 2 and 3, see detail at <https://docs.python.org/2/extending/embedding.html>.


Compile Options
---------------

gcc -o embedding\_example $(python3-config --cflags) $(python3-config --ldflags) embedding_example.c


Run
-----

```
yusenbindeMacBook-Pro:c justdoit$ ./embedding_example
Python version 3.6.0 (default, Mar 24 2017, 18:00:20)
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.42.1)].
Today is Thu Apr 27 18:49:15 2017
yusenbindeMacBook-Pro:c justdoit$
```


Uwsgi Python Plugin
====================

Uwsgi Python plugin supports wsgi protocol, which can be used to communicate between Python web project and container server.


Python Initialize
-----------------

```
int uwsgi_python_init() {

	char *pyversion = strchr(Py_GetVersion(), '\n');
	if (!pyversion) {
        	uwsgi_log_initial("Python version: %s\n", Py_GetVersion());
	}
	else {
        	uwsgi_log_initial("Python version: %.*s %s\n", pyversion-Py_GetVersion(), Py_GetVersion(), Py_GetCompiler()+1);
	}

	if (Py_IsInitialized()) {
		uwsgi_log("--- Python VM already initialized ---\n");
		PyGILState_Ensure();
		goto ready;
	}

	if (up.home != NULL) {
#ifdef PYTHREE
		// check for PEP 405 virtualenv (starting from python 3.3)
		char *pep405_env = uwsgi_concat2(up.home, "/pyvenv.cfg");
		if (uwsgi_file_exists(pep405_env)) {
			uwsgi_log("PEP 405 virtualenv detected: %s\n", up.home);
			free(pep405_env);
			goto pep405;
		}
		free(pep405_env);

		// build the PYTHONHOME wchar path
		wchar_t *wpyhome;
		size_t len = strlen(up.home) + 1; 
		wpyhome = uwsgi_calloc(sizeof(wchar_t) * len );
		if (!wpyhome) {
			uwsgi_error("malloc()");
			exit(1);
		}
		mbstowcs(wpyhome, up.home, len);
		Py_SetPythonHome(wpyhome);
		// do not free this memory !!!
		//free(wpyhome);
pep405:
#else
		Py_SetPythonHome(up.home);
#endif
		uwsgi_log("Set PythonHome to %s\n", up.home);
	}

	char *program_name = up.programname;
	if (!program_name) {
		program_name = uwsgi.binary_path;
	}

#ifdef PYTHREE
	if (!up.programname) {
		if (up.home) {
			program_name = uwsgi_concat2(up.home, "/bin/python");
		}
	}

	wchar_t *pname = uwsgi_calloc(sizeof(wchar_t) * (strlen(program_name)+1));
	mbstowcs(pname, program_name, strlen(program_name)+1);
	Py_SetProgramName(pname);
#else
	Py_SetProgramName(program_name);
#endif


	Py_OptimizeFlag = up.optimize;

	Py_Initialize();

ready:

	if (!uwsgi.has_threads) {
		uwsgi_log_initial("*** Python threads support is disabled. You can enable it with --enable-threads ***\n");
	}

	up.wsgi_spitout = PyCFunction_New(uwsgi_spit_method, NULL);
	up.wsgi_writeout = PyCFunction_New(uwsgi_write_method, NULL);

	up.main_thread = PyThreadState_Get();

        // by default set a fake GIL (little impact on performance)
        up.gil_get = gil_fake_get;
        up.gil_release = gil_fake_release;

        up.swap_ts = simple_swap_ts;
        up.reset_ts = simple_reset_ts;
	
#if defined(PYTHREE) || defined(Py_TPFLAGS_HAVE_NEWBUFFER)
	struct uwsgi_string_list *usl = NULL;
	uwsgi_foreach(usl, up.sharedarea) {
		uint64_t len = uwsgi_n64(usl->value);
		PyObject *obj = PyByteArray_FromStringAndSize(NULL, len);
        	char *storage = PyByteArray_AsString(obj);
		Py_INCREF(obj);
		struct uwsgi_sharedarea *sa = uwsgi_sharedarea_init_ptr(storage, len);
		sa->obj = obj;
	}
#endif

	uwsgi_log_initial("Python main interpreter initialized at %p\n", up.main_thread);

	return 1;

}
```

Reference
=========

  * <https://docs.python.org/3/extending/embedding.html>

  * <https://docs.python.org/2/extending/embedding.html>
