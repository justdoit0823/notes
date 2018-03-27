
gRPC
=====

gRPC is a grpc framework developed by google, which supports a lot of programming languages such as `C++`, `Java`, `Python`, `Go`, `Ruby`, `C#`, `Node.js`, `Android Java`, `Objective-C`, `PHP`.
The client communicates to the server with [HTTP/2](https://http2.github.io/) protocol. So it's decoupled, and easy to write client programs in a different language as the server.

For the more details, you can go to [What is gRPC](https://grpc.io/docs/guides/)


Run gRPC in multiprocess program
================================

Recently in grpcio 1.6.3, I got a problem when using gRPC in multiprocess Python program. If the channel is globally initialized, the gRPC call would hang in the child process. However the same program works well with grpcio 1.4.0 .
Later, I found something in gRPC's github issues, such as [gRPC Python 1.6.0 Library Incompatibility with `fork()`](https://github.com/grpc/grpc/issues/12455). From a contributor, I got some details.
>We intend to support fork() going forward for the 1.7 release.

>The 1.6 release introduced more background threads at the c-level, which are not carried over to child processes after the fork() call.

>In the interim, pinning grpcio==1.4.0 is the best workaround.

First, the gRPC essentially doesn't support `fork`, which means it doesn't guarantee safety in multiprocess programs. Second, more background threads introduced in 1.6 makes this problem arised.
But why a multithread program can't work correctly with `fork`?


Fork in multithread program
---------------------------

There is an old blog [deadlock-after-fork-in-python](https://github.com/justdoit0823/notes/blob/master/python/docs/deadlock-after-fork-in-python.md) about how a program works incorrectly after `fork` in Python.

### How gRPC behaves in different environments ###

  * macOS


```
grpc14 installed: grpcio==1.4.0,protobuf==3.4.0,six==1.11.0
grpc14 runtests: PYTHONHASHSEED='494489219'
grpc14 runtests: commands[0] | uname -a
Darwin yusenbindeMacBook-Pro.local 17.0.0 Darwin Kernel Version 17.0.0: Thu Aug 24 21:48:19 PDT 2017; root:xnu-4570.1.46~2/RELEASE_X86_64 x86_64
grpc14 runtests: commands[1] | python server.py
Greeter client start.
Greeter client received: Hello, you!

grpc16 installed: grpcio==1.6.0,protobuf==3.4.0,six==1.11.0
grpc16 runtests: PYTHONHASHSEED='494489219'
grpc16 runtests: commands[0] | uname -a
Darwin yusenbindeMacBook-Pro.local 17.0.0 Darwin Kernel Version 17.0.0: Thu Aug 24 21:48:19 PDT 2017; root:xnu-4570.1.46~2/RELEASE_X86_64 x86_64
grpc16 runtests: commands[1] | python server.py
Greeter client start.
call timeout.

grpc17 installed: grpcio==1.7.0,protobuf==3.4.0,six==1.11.0
grpc17 runtests: PYTHONHASHSEED='494489219'
grpc17 runtests: commands[0] | uname -a
Darwin yusenbindeMacBook-Pro.local 17.0.0 Darwin Kernel Version 17.0.0: Thu Aug 24 21:48:19 PDT 2017; root:xnu-4570.1.46~2/RELEASE_X86_64 x86_64
grpc17 runtests: commands[1] | python server.py
Greeter client start.
call timeout.
```

  * CentOS

```
grpc14 installed: grpcio==1.4.0,protobuf==3.4.0,six==1.11.0
grpc14 runtests: PYTHONHASHSEED='2780338798'
grpc14 runtests: commands[0] | uname -a
Linux iZ25wb48421Z 3.10.0-327.4.5.el7.x86_64 #1 SMP Mon Jan 25 22:07:14 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
grpc14 runtests: commands[1] | python server.py
Greeter client start.
Greeter client received: Hello, you!

grpc16 installed: grpcio==1.6.0,protobuf==3.4.0,six==1.11.0
grpc16 runtests: PYTHONHASHSEED='2780338798'
grpc16 runtests: commands[0] | uname -a
Linux iZ25wb48421Z 3.10.0-327.4.5.el7.x86_64 #1 SMP Mon Jan 25 22:07:14 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
grpc16 runtests: commands[1] | python server.py
Greeter client start.
call timeout.

grpc17 installed: grpcio==1.7.0,protobuf==3.4.0,six==1.11.0
grpc17 runtests: PYTHONHASHSEED='2780338798'
grpc17 runtests: commands[0] | uname -a
Linux iZ25wb48421Z 3.10.0-327.4.5.el7.x86_64 #1 SMP Mon Jan 25 22:07:14 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
grpc17 runtests: commands[1] | python server.py
Greeter client start.
Greeter client received: Hello, you!
```

  * Ubuntu

```

```

### The essence of fork ###

>The child process is created with a single thread—the one that called fork().
>The entire virtual address space of the parent is replicated in the child, including the states of mutexes, condition variables, and other pthreads objects.


So in a multithreading program, after fork, a child process is a single thread program with possible lock resources which were used in other nonexistent threads.
In some situation, this may be fortunately ok. Otherwise there is a big pitfall for you without attention.


Reference
=========

  * <https://github.com/grpc/grpc/blob/master/doc/environment_variables.md>

  * pstack

  * lldb

  * man fork
