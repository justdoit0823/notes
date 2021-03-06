
Variable in Python
==================


Variable is a name which refers to Python objects, and helps programmers write and read easily.
In general, there are two kinds of variables, which are `global` and `local`.
Global variable is defined at module level, while local variable is defined in a function body.
Here I will look into how local variable is resolved in a function.


Local variable
--------------

Usually we define a local variable with an assignment statement in a function,
and Python interpreter can easily know about this with lexical analysis.
Here is an example,

```
In [42]: def foo():
    ...:     a = 1231
    ...:

In [43]: foo.__code__.co_varnames
Out[43]: ('a',)

In [44]: foo.__code__.co_nlocals
Out[44]: 1
```

I have written a function called `foo`. It has only one statement which defines a local variable called `a`.
And we can get the name from the function's code object.

>co_varnames is a tuple containing the names of the local variables (starting with the argument names).
>co_nlocals is the number of local variables used by the function (including arguments).

Next, let's look at one more complex example,

```
In [45]: def bar(x, y):
    ...:     z = 123
    ...:     for i in range(10):
    ...:         print(z + i)
    ...:     g = 'haha'
    ...:     print(x, y, g)
    ...:

In [46]: bar.__code__.co_varnames
Out[46]: ('x', 'y', 'z', 'i', 'g')

In [47]: bar.__code__.co_nlocals
Out[47]: 5
```

There are five unique local variables. After analysis, the order of these variables is determined.
When the function is executed, name is converted to local variable's order.
We can verify this with disassembled bytecode.


Cell variable
-------------

>co_cellvars is a tuple containing the names of local variables that are referenced by nested functions.


From python's official website, I know the cell variable is related to [closure](https://en.wikipedia.org/wiki/Closure_(computer_programming)).
And the following is an example about how closure works,


```
In [48]: def foo_cell():
    ...:     x = 123
    ...:     def sub_foo():
    ...:         print(x)
    ...:         y = 1231
    ...:

In [49]: foo_cell.__code__.co_varnames
Out[49]: ('sub_foo',)

In [50]: foo_cell.__code__.co_nlocals
Out[50]: 1

In [51]: foo_cell.__code__.co_cellvars
Out[51]: ('x',)
```


Variable `x` is defined in the scope of `foo_cell` function. As referred in the inner function `sub_foo`, variable `x` is marked as a cell variable rather than a local variable. It has special opcodes to load and store variable.


Free variable
-------------

>co_freevars is a tuple containing the names of free variables.

Haha, these words make no sense. We still cannot catch the truth of free variable.
But we can get some information from the function's code object.

```
In [53]: def foo_free():
    ...:     x = 123
    ...:     def sub_foo():
    ...:         print(x)
    ...:         y = 1231
    ...:     return sub_foo

In [60]: foo_free()
Out[60]: <function __main__.foo_free.<locals>.sub_foo>

In [61]: Out[60].__code__.co_freevars
Out[61]: ('x',)

In [66]: Out[60].__closure__[0].cell_contents
Out[66]: 123
```

The free variable is a variable which refers to the value in cell variables of the outside function.


Now, it's clear that the local variable is a common variable. The cell variable is referred in the inside function as a part of the closure.
And the free variable refers to the cell variable in the outside function.


Variable Layout
===============

Variable layout
---------------

In the CPython implementation, the local variables are allocated as the following,

  * local variables

  * cell variables

  * free variables

  * stack values


These variables are located in an array of object pointers. The beginning is the local variables, and the end is the stack values.
It's determined when the lexical analysis is finished.


>co_stacksize is the required stack size (including local variables).


This is the max stack size required to execute related function, and the max sized values can be pushed onto the stack.


Pitfall in the colusre
----------------------

Free variable is different from the local variable in which it refers to the cell index rather than the cell variable's instant value.
Once the variable's value is changed, the free variable also points to the new value through the cell index. For example,


```
In [67]: def closure_pitfall():
    ...:     sub_f_list = []
    ...:     for i in range(5):
    ...:         sub_f_list.append(lambda : print(i))
    ...:     for f in sub_f_list:
    ...:         f()
    ...:

In [68]: closure_pitfall()
4
4
4
4
4
```


It's amazing. We had believed that the variable `i` in each function should refer to the number from zero to four when writing in this way.
In fact, the variable `i` points to the latest number four after it's changed. Sometimes this may lead to bugs.


**We should notice that the cell variable has no snapshot each time when the free variable refers to it.
And the free variable always points to the latest value of the related cell variable.**


Reference
=========

  * <https://docs.python.org/3/reference/datamodel.html#objects-values-and-types>

  * <https://en.wikipedia.org/wiki/Closure_(computer_programming)>
