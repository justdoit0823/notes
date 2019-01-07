
Java
====

Method
=======

Argument
--------

Arguments defined in Java methods are called by value, while object's reference value can modify its state.
For example,

  * Primitive type

Primitive type argument is called by value, we can't modify the argument's state within the method.

  * Object type

Object type argument is also called by value, but the value is an object reference which could be used to access the original object within the method.


Generics
========

  * compile time type check

  * type erasure

  * one compiled version of a generic class


Concurrency
===========

Runnable
----------

  * a common interface

  * implements `run` method

  * `run` method has no arguments

  * `run` method has no result


Callable
--------

  * a generic interface with result type

  * implements `call` method

  * `call` method has no arguments

  * `call` method has specified result type, throws `Exception` otherwise


Reference
=========

  * <https://en.wikipedia.org/wiki/Generics_in_Java>
