
super
=====

A built-in Python function returns a proxy object that delegates method calls to a parent or sibling class of type.

It is useful for accessing inherited methods that have been overridden in a class.

The search order is same as that used by getattr() except that the type itself is skipped.


Signature
---------

super(self, /, *args, **kwargs)


Arguments
------------

  * No param

super() as a new super, same as super(__class__, <first argument>), see [PEP3135](https://www.python.org/dev/peps/pep-3135/).

  * One type param

super(type), returns a unbound super object.

  * Type param and object param

super(type, obj), returns a bound super object and requires isinstance(obj, type).

  * Two type params

super(type, type2), returns a bound super object and requires issubclass(type2, type).


Usage
=====


Implementation
==============


super_init
----------

```
static int
super_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    superobject *su = (superobject *)self;
    PyTypeObject *type = NULL;
    PyObject *obj = NULL;
    PyTypeObject *obj_type = NULL;

    if (!_PyArg_NoKeywords("super", kwds))
        return -1;
    if (!PyArg_ParseTuple(args, "|O!O:super", &PyType_Type, &type, &obj))
        return -1;

    if (type == NULL) {
        /* Call super(), without args -- fill in from __class__
           and first local variable on the stack. */
        PyFrameObject *f;
        PyCodeObject *co;
        Py_ssize_t i, n;
        f = PyThreadState_GET()->frame;
        if (f == NULL) {
            PyErr_SetString(PyExc_RuntimeError,
                            "super(): no current frame");
            return -1;
        }
        co = f->f_code;
        if (co == NULL) {
            PyErr_SetString(PyExc_RuntimeError,
                            "super(): no code object");
            return -1;
        }
        if (co->co_argcount == 0) {
            PyErr_SetString(PyExc_RuntimeError,
                            "super(): no arguments");
            return -1;
        }
        obj = f->f_localsplus[0];
        if (obj == NULL && co->co_cell2arg) {
            /* The first argument might be a cell. */
            n = PyTuple_GET_SIZE(co->co_cellvars);
            for (i = 0; i < n; i++) {
                if (co->co_cell2arg[i] == 0) {
                    PyObject *cell = f->f_localsplus[co->co_nlocals + i];
                    assert(PyCell_Check(cell));
                    obj = PyCell_GET(cell);
                    break;
                }
            }
        }
        if (obj == NULL) {
            PyErr_SetString(PyExc_RuntimeError,
                            "super(): arg[0] deleted");
            return -1;
        }
        if (co->co_freevars == NULL)
            n = 0;
        else {
            assert(PyTuple_Check(co->co_freevars));
            n = PyTuple_GET_SIZE(co->co_freevars);
        }
        for (i = 0; i < n; i++) {
            PyObject *name = PyTuple_GET_ITEM(co->co_freevars, i);
            assert(PyUnicode_Check(name));
            if (_PyUnicode_EqualToASCIIId(name, &PyId___class__)) {
                Py_ssize_t index = co->co_nlocals +
                    PyTuple_GET_SIZE(co->co_cellvars) + i;
                PyObject *cell = f->f_localsplus[index];
                if (cell == NULL || !PyCell_Check(cell)) {
                    PyErr_SetString(PyExc_RuntimeError,
                      "super(): bad __class__ cell");
                    return -1;
                }
                type = (PyTypeObject *) PyCell_GET(cell);
                if (type == NULL) {
                    PyErr_SetString(PyExc_RuntimeError,
                      "super(): empty __class__ cell");
                    return -1;
                }
                if (!PyType_Check(type)) {
                    PyErr_Format(PyExc_RuntimeError,
                      "super(): __class__ is not a type (%s)",
                      Py_TYPE(type)->tp_name);
                    return -1;
                }
                break;
            }
        }
        if (type == NULL) {
            PyErr_SetString(PyExc_RuntimeError,
                            "super(): __class__ cell not found");
            return -1;
        }
    }

    if (obj == Py_None)
        obj = NULL;
    if (obj != NULL) {
        obj_type = supercheck(type, obj);
        if (obj_type == NULL)
            return -1;
        Py_INCREF(obj);
    }
    Py_INCREF(type);
    Py_XSETREF(su->type, type);
    Py_XSETREF(su->obj, obj);
    Py_XSETREF(su->obj_type, obj_type);
    return 0;
}

```

supercheck
----------

```
static PyTypeObject *
supercheck(PyTypeObject *type, PyObject *obj)
{
    /* Check that a super() call makes sense.  Return a type object.

       obj can be a class, or an instance of one:

       - If it is a class, it must be a subclass of 'type'.      This case is
         used for class methods; the return value is obj.

       - If it is an instance, it must be an instance of 'type'.  This is
         the normal case; the return value is obj.__class__.

       But... when obj is an instance, we want to allow for the case where
       Py_TYPE(obj) is not a subclass of type, but obj.__class__ is!
       This will allow using super() with a proxy for obj.
    */

    /* Check for first bullet above (special case) */
    if (PyType_Check(obj) && PyType_IsSubtype((PyTypeObject *)obj, type)) {
        Py_INCREF(obj);
        return (PyTypeObject *)obj;
    }

    /* Normal case */
    if (PyType_IsSubtype(Py_TYPE(obj), type)) {
        Py_INCREF(Py_TYPE(obj));
        return Py_TYPE(obj);
    }
    else {
        /* Try the slow way */
        PyObject *class_attr;

        class_attr = _PyObject_GetAttrId(obj, &PyId___class__);
        if (class_attr != NULL &&
            PyType_Check(class_attr) &&
            (PyTypeObject *)class_attr != Py_TYPE(obj))
        {
            int ok = PyType_IsSubtype(
                (PyTypeObject *)class_attr, type);
            if (ok)
                return (PyTypeObject *)class_attr;
        }

        if (class_attr == NULL)
            PyErr_Clear();
        else
            Py_DECREF(class_attr);
    }

    PyErr_SetString(PyExc_TypeError,
                    "super(type, obj): "
                    "obj must be an instance or subtype of type");
    return NULL;
}
```

super_getattro
--------------

```
static PyObject *
super_getattro(PyObject *self, PyObject *name)
{
    superobject *su = (superobject *)self;
    PyTypeObject *starttype;
    PyObject *mro;
    Py_ssize_t i, n;

    starttype = su->obj_type;
    if (starttype == NULL)
        goto skip;

    /* We want __class__ to return the class of the super object
       (i.e. super, or a subclass), not the class of su->obj. */
    if (PyUnicode_Check(name) &&
        PyUnicode_GET_LENGTH(name) == 9 &&
        _PyUnicode_EqualToASCIIId(name, &PyId___class__))
        goto skip;

    mro = starttype->tp_mro;
    if (mro == NULL)
        goto skip;

    assert(PyTuple_Check(mro));
    n = PyTuple_GET_SIZE(mro);

    /* No need to check the last one: it's gonna be skipped anyway.  */
    for (i = 0; i+1 < n; i++) {
        if ((PyObject *)(su->type) == PyTuple_GET_ITEM(mro, i))
            break;
    }
    i++;  /* skip su->type (if any)  */
    if (i >= n)
        goto skip;

    /* keep a strong reference to mro because starttype->tp_mro can be
       replaced during PyDict_GetItem(dict, name)  */
    Py_INCREF(mro);
    do {
        PyObject *res, *tmp, *dict;
        descrgetfunc f;

        tmp = PyTuple_GET_ITEM(mro, i);
        assert(PyType_Check(tmp));

        dict = ((PyTypeObject *)tmp)->tp_dict;
        assert(dict != NULL && PyDict_Check(dict));

        res = PyDict_GetItem(dict, name);
        if (res != NULL) {
            Py_INCREF(res);

            f = Py_TYPE(res)->tp_descr_get;
            if (f != NULL) {
                tmp = f(res,
                    /* Only pass 'obj' param if this is instance-mode super
                       (See SF ID #743627)  */
                    (su->obj == (PyObject *)starttype) ? NULL : su->obj,
                    (PyObject *)starttype);
                Py_DECREF(res);
                res = tmp;
            }

            Py_DECREF(mro);
            return res;
        }

        i++;
    } while (i < n);
    Py_DECREF(mro);

  skip:
    return PyObject_GenericGetAttr(self, name);
}
```

Reference
=========

  * <https://docs.python.org/3/library/functions.html#super>

  * <https://www.python.org/dev/peps/pep-3135/>
