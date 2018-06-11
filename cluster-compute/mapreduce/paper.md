
MapReduce
=========

MapReduce is a programming model and an associated implementation for processing and generating large data sets. Users specify a map function that processes a key/value pair to generate a set of intermediate key/value pairs, and a reduce function that merges all intermediate values associated with the same intermediate key.


Primitives
----------

  * Map

Map, written by the user, takes an input pair and produces a set of intermediate key/value pairs.
The MapReduce library groups together all intermediate values associated with the same intermediate key I and passes them to the Reduce function.

  * Reduce

The Reduce function, also written by the user, accepts an intermediate key I and a set of values for that key. It merges together these values to form a possibly smaller set of values.


Phase
-----

  * Map

A worker who is assigned a map task reads the contents of the corresponding input split. It parses key/value pairs out of the input data and passes each pair to the user-defined Map function. The intermediate key/value pairs produced by the Map function are buffered in memory.

  * Reduce

When a reduce worker has read all intermediate data, it sorts it by the intermediate keys so that all occurrences of the same key are grouped together. The sorting is needed because typically many different keys map to the same reduce task.
The reduce worker iterates over the sorted intermediate data and for each unique intermediate key encountered, it passes the key and the corresponding set of intermediate values to the user’s Reduce func- tion. The output of the Reduce function is appended to a final output file for this reduce partition.


Worker
-------

There are M map tasks and R reduce tasks to assign. The master picks idle workers and assigns each one a map task or a reduce task.

  * Mater

The master worker schedules the map and reduce tasks.

  * Task worker

The task worker executes the assigned tasks.


Data
------

  * Input file

The MapReduce library in the user program first splits the input files into M pieces of typically 16 megabytes to 64 megabytes (MB) per piece (controllable by the user via an optional parameter).

  * Intermediate file

The intermediate key/value pairs produced by the Map function are buffered in memory. Periodically, the buffered pairs are written to local disk, partitioned into R regions by the partitioning function.
So there are finally `M x R` intermediate files, which will be used by the reduce worker later.
The reduce worker uses remote procedure calls to read the related buffered data from the local disks of the map workers.


Fault Tolerance
---------------

  * Worker failure

The master pings every worker periodically. If no response is received from a worker in a certain amount of time, the master marks the worker as failed. Any map tasks completed by the worker are reset back to their initial idle state, and therefore become eligible for scheduling on other workers. Similarly, any map task or reduce task in progress on a failed worker is also reset to idle and becomes eligible for rescheduling.


  * Master failure

Current implementation aborts the MapReduce computation if the master fails. Clients can check for this condition and retry the MapReduce operation if they desire.


  * Semantics in the Presence of Failures

When the user-supplied map and reduce operators are deterministic functions of their input values, our distributed implementation produces the same output as would have been produced by a non-faulting sequential execution of the entire program.
MapReduce relies on atomic commits of map and reduce task outputs to achieve this property.


Reference
---------

  * <https://pdos.csail.mit.edu/6.824/papers/mapreduce.pdf>
