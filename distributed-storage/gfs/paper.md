
GFS
===

A scalable distributed file system for large distributed data-intensive applications.
It provides fault tolerance while running on inexpensive commodity hardware,
and it delivers high aggregate performance to a large number of clients.


Architecture
------------

In the GFS cluster, there are mainly two components `master` and `chunckserver`.
Each file has an identified path, and is divided into several chuncks within the cluster.


### master ###

  * create a file atomically

  * record file and chunck namespaces

  * record chunckservers locations

  * map a file with chunck index to chunck handle and server location

  * support persistent data checkpoint with operation log


### chunckservers ###

  * store chunck data

  * interacts with clients directly

  * no server level data cache


Each chunck has an immutable and globally unique 64 bit chunck handle, and is a plain linux file with a fixed size, such as 64M.
For reliability, each chunck has n replics on other chunckservers.


Consistency model
------------------

  * consistent

A file region is `consistent` if all clients will always see the same data, regardless of which replicas they read from.

  * defined

A file region is `defined` after a file data mutation if it is consistent and clients will see what the mutation writes in its entirety.


### data mutation ###

File namespace mutations (e.g., file creation) are atomic.


Data mutations may be writes or record appends. A write causes data to be written at an application-specified file offset.
A record append causes data (the “record”) to be appended atomically at least once even in the presence of concurrent mutations, but at an offset of GFS’s choosing.


There are two kinds of mutation models as the following,

  * serial successful mutations

It's defined and consistent.

  * concurrent successful mutations

It's undefined but consistent.


According to the above, all mutations are consistent, but may lead to undefined result when writing concurrently.


Reference
=========

  * <https://pdos.csail.mit.edu/6.824/papers/gfs.pdf>
