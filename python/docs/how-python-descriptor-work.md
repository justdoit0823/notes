
Python Descriptor
=================

	Descriptor是Python中一个极其重要的特性, 控制属性的访问。基于此, 衍生出了很多黑魔法。


CPython属性访问实现
===================


* 读属性流程

		PyObject *
		_PyObject_GenericGetAttrWithDict(PyObject *obj, PyObject *name, PyObject *dict)
		{
			// 获取obj的类型
			PyTypeObject *tp = Py_TYPE(obj);
			PyObject *descr = NULL;
			PyObject *res = NULL;
			descrgetfunc f;
			Py_ssize_t dictoffset;
			PyObject **dictptr;

			if (!PyUnicode_Check(name)){
				PyErr_Format(PyExc_TypeError,
							 "attribute name must be string, not '%.200s'",
							 name->ob_type->tp_name);
				return NULL;
			}
			else
				Py_INCREF(name);

			if (tp->tp_dict == NULL) {
				if (PyType_Ready(tp) < 0)
					goto done;
			}

			// 获取类型中对应的属性descr
			descr = _PyType_Lookup(tp, name);
			Py_XINCREF(descr);

			f = NULL;
			if (descr != NULL) {
				// 获取get descriptor并且判断是否为数据描述符
				f = descr->ob_type->tp_descr_get;
				if (f != NULL && PyDescr_IsData(descr)) {
					res = f(descr, obj, (PyObject *)obj->ob_type);
					goto done;
				}
			}

			if (dict == NULL) {
				/* Inline _PyObject_GetDictPtr */
				dictoffset = tp->tp_dictoffset;
				if (dictoffset != 0) {
					if (dictoffset < 0) {
						Py_ssize_t tsize;
						size_t size;

						tsize = ((PyVarObject *)obj)->ob_size;
						if (tsize < 0)
							tsize = -tsize;
						size = _PyObject_VAR_SIZE(tp, tsize);

						dictoffset += (long)size;
						assert(dictoffset > 0);
						assert(dictoffset % SIZEOF_VOID_P == 0);
					}
					dictptr = (PyObject **) ((char *)obj + dictoffset);
					dict = *dictptr;
				}
			}
			if (dict != NULL) {
				Py_INCREF(dict);

				// 在obj的__dict__中进行查找
				res = PyDict_GetItem(dict, name);
				if (res != NULL) {
					Py_INCREF(res);
					Py_DECREF(dict);
					goto done;
				}
				Py_DECREF(dict);
			}

			if (f != NULL) {
				// 通过非数据描述符的方式获取属性
				res = f(descr, obj, (PyObject *)Py_TYPE(obj));
				goto done;
			}

			if (descr != NULL) {
				res = descr;
				descr = NULL;
				goto done;
			}

			PyErr_Format(PyExc_AttributeError,
						 "'%.50s' object has no attribute '%U'",
						 tp->tp_name, name);
		  done:
			Py_XDECREF(descr);
			Py_DECREF(name);
			return res;
		}


* 写属性流程

		int
		_PyObject_GenericSetAttrWithDict(PyObject *obj, PyObject *name,
										 PyObject *value, PyObject *dict)
		{
			// 获取obj的类型
			PyTypeObject *tp = Py_TYPE(obj);
			PyObject *descr;
			descrsetfunc f;
			PyObject **dictptr;
			int res = -1;

			if (!PyUnicode_Check(name)){
				PyErr_Format(PyExc_TypeError,
							 "attribute name must be string, not '%.200s'",
							 name->ob_type->tp_name);
				return -1;
			}

			if (tp->tp_dict == NULL && PyType_Ready(tp) < 0)
				return -1;

			Py_INCREF(name);

		    // 查找类型中对应的属性
			descr = _PyType_Lookup(tp, name);
			Py_XINCREF(descr);

			f = NULL;
			if (descr != NULL) {

		        // 获取set descriptor判断是否为数据描述符并且写属性
				f = descr->ob_type->tp_descr_set;
				if (f != NULL && PyDescr_IsData(descr)) {
					res = f(descr, obj, value);
					goto done;
				}
			}

			if (dict == NULL) {
				dictptr = _PyObject_GetDictPtr(obj);
				if (dictptr != NULL) {
					res = _PyObjectDict_SetItem(Py_TYPE(obj), dictptr, name, value);
					if (res < 0 && PyErr_ExceptionMatches(PyExc_KeyError))
						PyErr_SetObject(PyExc_AttributeError, name);
					goto done;
				}
			}
			if (dict != NULL) {
				Py_INCREF(dict);

		        // 通过obj的__dict__进行属性操作
				if (value == NULL)
					res = PyDict_DelItem(dict, name);
				else
					res = PyDict_SetItem(dict, name, value);
				Py_DECREF(dict);
				if (res < 0 && PyErr_ExceptionMatches(PyExc_KeyError))
					PyErr_SetObject(PyExc_AttributeError, name);
				goto done;
			}

			if (f != NULL) {

		        // 以非数据描述符方式写属性
				res = f(descr, obj, value);
				goto done;
			}

			if (descr == NULL) {
				PyErr_Format(PyExc_AttributeError,
							 "'%.100s' object has no attribute '%U'",
							 tp->tp_name, name);
				goto done;
			}

			PyErr_Format(PyExc_AttributeError,
						 "'%.50s' object attribute '%U' is read-only",
						 tp->tp_name, name);
		  done:
			Py_XDECREF(descr);
			Py_DECREF(name);
			return res;
		}


* 属性访问顺序

		data descriptor -> obj dict -> non data descriptor
		详细的可以在python官网文档<https://docs.python.org/3/reference/datamodel.html#invoking-descriptors>查看.


常见的实现
----------

* instancemethod(隐含)

* classmethod

* staticmethod

* property


参考
----

* 代码见Python3源码中/Objects/object.c中

* 文档细节见<https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access>
