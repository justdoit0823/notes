
死锁
====

定义
----

关于死锁的定义，摘自维基如下：

> 当两个以上的运算单元，双方都在等待对方停止运行，以获取系统资源，但是没有一方提前退出时，就称为死锁。
> 在多任务操作系统中，操作系统为了协调不同进程，能否获取系统资源时，为了让系统运作，必须要解决这个问题。

详见<https://zh.wikipedia.org/wiki/%E6%AD%BB%E9%94%81>


场景复现
--------

### 多进程多线程日志输出 ###

使用Python标准库中提供的logging系统时，日志输出是线程安全的，但是系统提供的write（2）是非线程安全的，所以在Handler的内部实现里隐藏了锁。

在多进程多线程场景下，如果A线程里做了日志输出的操作，B线程里面执行了fork（2）系统调用，在子线程中用同样的Handler输出日志时会有一定的概率出现死锁。

关于这个问题，SO上面有个讨论的帖子<https://stackoverflow.com/questions/24509650/deadlock-with-logging-multiprocess-multithread-python-script>，

基于这个帖子Python社区里有一个关于fork时避免死锁的patch，具体见<http://bugs.python.org/issue6721>


### 多进程多线程dns查询 ###

Python中提供的dns查询操作API`socket.getaddrinfo`同样是线程安全的，而且是全局唯一安全，然而系统API中有些是线程安全的，系统API本身隐藏了带锁的实现；有些不是的，Python中会做带锁的实现。

在多进程多线程场景下，如果A线程中进行了dns查询操作或者网络请求，B线程里面执行了fork（2）系统调用，在子进程中发起dns查询操作，同样会有一定的概率出现死锁。


上面的两种操作有可能是自己显式发生的，也有可能是隐式发生的（调用网络库），死锁的结果以一定的概率出现。


### 复现代码 ###

复现代码很容易，在gist上贴了一份儿，具体见<https://gist.github.com/justdoit0823/5b3eb31bb4f08aba42bbd56ec1a0a552>。


死锁的原因
==========

fork
----

fork（2）是类unix系统上创建新进程的一个系统调用，Python在自己的os模块中暴露了这个方法，针对系统调用做了一个封装。

通过fork创建一个子进程后，子进程会被分配一个新的PID，创建一个线程，实际上是复制父进程中调用fork的线程程；还会复制父进程的全部虚拟地址空间，包括互斥锁、条件变量和其它线程对象的状态；另外，还有其它如文件描述符等。

这里的重点是会复制父进程中锁的状态，这意味着fork时未释放的锁状态会被复制到子进程中，然而拥有锁的线程在新的进程中并不存在，导致新进程中获取锁资源的时候发生了死锁。

为了解决这个问题，系统提供了一个pthread_atfork操作，可以注册handler在fork不同阶段执行特定的清理和初始化动作。

然而目前这个API并没有被移植到Python的正式版中，但是在Python3.7中引入了一个新的模块atfork来解决这个问题，具体见<https://bugs.python.org/issue16500>。引入之后也并不能完全解决问题，因为很难去完全清理引用了锁，特别是使用众多的库。

另外，纠正一个概念，有些书上写fork调用一次返回两次，模糊父子进程，这个说法并不准确；应该fork调用之后在各自进程中以不同的值返回，就是正常的返回结果，只不过是在两个进程中。


锁的构成
--------

在Python进程中存在两种锁，一是C代码中包含的锁如mutex，另外就是Python中提供的锁如Lock。本质上是一种锁存在，因为Lock的实现是mutext加上condition variable。

所以进程fork时，两种锁都会被复制到新的子进程中，影响后续的锁操作。


Python中的锁
============

Lock
----

在Python中，Lock是同时只能被一个线程获取到，但是却可以被其它线程释放。

> The class implementing primitive lock objects. Once a thread has acquired a lock, subsequent attempts to acquire it block, until it is released; any thread may release it.


RLock
-----

在Python中，Lock是同时只能被一个线程获取到，并且可以被多次获取，最外层的释放操作之后才会处于释放状态。

> This class implements reentrant lock objects. A reentrant lock must be released by the thread that acquired it. Once a thread has acquired a reentrant lock, the same thread may acquire it again without blocking; the thread must release it once for each time it has acquired it.

引用
====

  * <https://zh.wikipedia.org/wiki/%E6%AD%BB%E9%94%81>

  * <https://stackoverflow.com/questions/24509650/deadlock-with-logging-multiprocess-multithread-python-script>

  * <http://bugs.python.org/issue6721>

  * <https://bugs.python.org/issue16500>

  * <https://github.com/google/python-atfork>

  * <https://docs.python.org/3/library/threading.html#lock-objects>

  * man 2 fork

  * man 3 fork

  * man pthread_atfork
