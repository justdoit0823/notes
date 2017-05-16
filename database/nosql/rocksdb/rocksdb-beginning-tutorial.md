
RocksDB
=======

[RocksDB](http://rocksdb.org/) is a C++ library that provides an embeddable, persistent key-value store for fast storage.

It's keys and values are arbitrary byte streams.


How to Try
============

Get RocksDB
-----------

```
# can access github with ssh
git clone git@github.com:facebook/rocksdb.git

# access github by http
git clone https://github.com/facebook/rocksdb.git
```

Install
-------

On Mac OSX, you can simply install RocksDB with command `brew install rocksdb`. On other platforms, there maybe some package managers doing the same work.

Read more detail at <https://github.com/facebook/rocksdb/blob/master/INSTALL.md>.


### Dependencies ###

  * zlib

  * bzip2

  * snappy

  * zstandard

  * gflags


### Make options ###


  * make static_lib

Compile RocksDB as a shared libary. It's recommended to use this make option, especilly in production environment.

  * make shared_lib

Compile RocksDB as a shared libary in release mode.


  * make check

Compile RocksDB in debug mode and run all unit tests.

  * make all

Compile RockDB as a static libary in debug mode, compile all tools, and run all unit tests. Don't use this in production.


How to start with command line
==============================

rocksdb_ldb
-------------

A simple command line LevelDB tool and support regular rocksdb operations.

Initialize rocksdb database and do data access commands like put, get, delete.

```
(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 --create_if_missing put foo bar
OK

(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 get foo
bar

(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 delete foo
OK

(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 get foo
Failed: NotFound:
(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 put foo1 bar1
OK

(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 get foo1
bar1

```

Starts a REPL shell for querying keys in database.

```
(v3.6) yusenbindeMacBook-Pro:rocksdb justdoit$ rocksdb_ldb --db=/Users/justdoit/workspace/rocksdb/data/test_db1 query
help
get <key>
put <key> <value>
delete <key>
get foo
Not found foo
get foo1
foo1 ==> bar1
delete foo1
Successfully deleted foo1
put foo2 bar
Successfully put foo2 bar
get foo2
foo2 ==> bar
^D
```

Reference
=========

  * <https://github.com/facebook/rocksdb/wiki>
