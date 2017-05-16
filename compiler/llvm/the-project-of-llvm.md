
LLVM
====

The LLVM Project is a collection of modular and reuseable compiler and toolchain technologies.


How to Install
--------------

It's easy to install with platform package manager, like brew on Mac OSX and the command `brew install llvm`.


Sub Projects
------------

  * LLVM core libaries

The libaries provide a morden source and target independent optimizer, along with code generation support for many popular CPUs.


  * Clang

Clang is an "LLVM native" C/C++/Objective-C compiler.


  * dragonegg

Dragonegg integrates the LLVM optimizers and code generator with GCC parsers.


  * LLDB

The LLDB project build on libaries provided by LLVM and Clang to provide a great native debugger.


  * libc++ & libc++ ABI

The libc++ and libc++ ABI projects provide a standard conformant and high-performance implementation of the C++ standard libary, including full support of C++ 11.


  * compile-rt

The compiler-rt project provides highly tuned implementations of the low-level code generator support routines like "__fixunsdfdi" and other calls generated when a target doesn't have a short sequence of native instructions to implement a core IR operation.


  * OpenMP

The OpenMP subproject provides an OpenMP runtime for use with the OpenMP implementation in Clang.


  * vmkit

The vmkit project is an implementation of the Java and .NET Virtual Machines that is built on LLVM technologies.


  * polly

The polly project implements a suite of cache-locality optimizations as well as auto-parallelism and vectorization using a polyhedral model.


  * libclc

The libclc project aims to implement the OpenCL standard library.


  * klee

The klee project implements a "symbolic virtual machine" which uses a theorem prover to try to evaluate all dynamic paths through a program in an effort to find bugs and to prove properties of functions.


  * SAFECode

The SAFECode project is a memory safety compiler for C/C++ programs.


LLVM Core
=========

Read more detail at <http://llvm.org/docs/> and <http://www.aosabook.org/en/llvm.html>.


References
==========

  * <http://llvm.org/>

  * <http://llvm.org/docs/>

  * <http://www.aosabook.org/en/llvm.html>
