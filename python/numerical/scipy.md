
SciPy library
=============

Fundamental library for scientific computing.


Numerical
=========

Integration
------------

The `scipy.integrate` module provides `quad`, `dblquad`, `tplquad` etc.
For example, calculating a general purpose integration.

```python
from scipy.integrate import quad

f = lambda x: x ** 2

i = quad(f, 0, 1)
print(i, (1 ** 3) / 3)
```

Read more detail at [Integration](http://scipy.github.io/devdocs/tutorial/integrate.html).

### Methods ###

There is a [Numerical integration](https://en.wikipedia.org/wiki/Numerical_integration) wiki page about integration methods,
and a FORTRAN library [QUADPACK](https://en.wikipedia.org/wiki/QUADPACK).


Derivative
-----------

The `scipy.misc.derivative` function supports to find the n-th derivative of a function at a point.
For example, calculating a derivative of a simple function.

```python
from scipy.misc import derivative

f = lambda x: x ** 3 + x ** 2

d = derivative(f, 1.0, dx=1e-6)
print(d, 3 * (1.0 ** 2) + 2 * 1.0)
```

Read more detail at [Derivative](http://scipy.github.io/devdocs/generated/scipy.misc.derivative.html#scipy.misc.derivative).


### Difference ###


[Finite difference](https://en.wikipedia.org/wiki/Finite_difference) is a wiki page about commonly considered difference forms and relation with derivative.

[Finite difference method](https://en.wikipedia.org/wiki/Finite_difference_method) is a wiki page about difference methods.


Performance
===========

Paralle
-------

  * Use parallel primitives

  * Write multithreaded or multiprocess code


Read more detail at [Parallel Programming with numpy and scipy](https://scipy.github.io/old-wiki/pages/ParallelProgramming).


### Numpy parallel ###

the relative macro definition,

```c
#if NPY_ALLOW_THREADS
#define NPY_BEGIN_ALLOW_THREADS Py_BEGIN_ALLOW_THREADS
#define NPY_END_ALLOW_THREADS Py_END_ALLOW_THREADS
#define NPY_BEGIN_THREADS do {_save = PyEval_SaveThread();} while (0);
#define NPY_END_THREADS   do { if (_save) \
                { PyEval_RestoreThread(_save); _save = NULL;} } while (0);
#define NPY_BEGIN_THREADS_THRESHOLDED(loop_size) do { if (loop_size > 500) \
                { _save = PyEval_SaveThread();} } while (0);

#define NPY_BEGIN_THREADS_DESCR(dtype) \
        do {if (!(PyDataType_FLAGCHK(dtype, NPY_NEEDS_PYAPI))) \
                NPY_BEGIN_THREADS;} while (0);

#define NPY_END_THREADS_DESCR(dtype) \
        do {if (!(PyDataType_FLAGCHK(dtype, NPY_NEEDS_PYAPI))) \
                NPY_END_THREADS; } while (0);
```

the internal operation example,

```c
NPY_BEGIN_THREADS_DESCR(PyArray_DESCR(ap2));
while (it1->index < it1->size) {
	while (it2->index < it2->size) {
		dot(it1->dataptr, is1, it2->dataptr, is2, op, l, NULL);
		op += os;
        PyArray_ITER_NEXT(it2);
    }
	PyArray_ITER_NEXT(it1);
	PyArray_ITER_RESET(it2);
}
NPY_END_THREADS_DESCR(PyArray_DESCR(ap2));
```


BLAS
----

Read more detail at [Basic Linear Algebra Subprograms](https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms).


Reference
==========

  * <https://en.wikipedia.org/wiki/Numerical_integration>

  * <https://en.wikipedia.org/wiki/QUADPACK>

  * <https://en.wikipedia.org/wiki/Finite_difference>

  * <https://en.wikipedia.org/wiki/Finite_difference_method>

  * <http://scipy.github.io/devdocs/index.html>

  * <https://scipy.github.io/old-wiki/pages/ParallelProgramming>

  * <https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms>
