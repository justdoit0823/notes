
PostgreSQL
==========

PostgreSQL is an object-relational database management system (ORDBMS) based on POSTGRES, Version 4.2, developed at the University of California at Berkeley Computer Science Department.
POSTGRES pioneered many concepts that only became available in some commercial database systems much later.

Modern features
-------------------

  * complex queries

  * foreign keys

  * triggers

  * updatable views

  * transactional integrity

  * multiversion concurrency control


How to extend PostgreSQL
------------------------

  * data types

  * functions

  * operators

  * aggregate functions

  * index methods

  * procedural languages


License
-------

The PostgreSQL license is liberal. It's free for everyone who wants to use, modify and distribute PostgreSQL for any purpose.


Architecture
============

Multi process
-------------

PostgreSQL server is a multi process architecture, which is consisted of the following processes.

  * postgres master

  * wal writer

  * bgwriter

  * checkpointer

  * autovacuum

  * stats collector

Every client connection is handled by the child process.


Transaction
===========

MVCC
----

PostgreSQL provides a rich set of tools for developers to manage concurrent access to data. Internally, data consistency is maintained by using a multiversion model (Multiversion Concurrency Control, MVCC).
This means that each SQL statement sees a snapshot of data (a database version) as it was some time ago, regardless of the current state of the underlying data.
This prevents statements from viewing inconsistent data produced by concurrent transactions performing updates on the same data rows, providing transaction isolation for each database session. MVCC, by eschewing the locking methodologies of traditional database systems, minimizes lock contention in order to allow for reasonable performance in multiuser environments.

The main advantage of using the MVCC model of concurrency control rather than locking is that in MVCC locks acquired for querying (reading) data do not conflict with locks acquired for writing data, and so reading never blocks writing and writing never blocks reading. PostgreSQL maintains this guarantee even when providing the strictest level of transaction isolation through the use of an innovative Serializable Snapshot Isolation (SSI) level.

Table- and row-level locking facilities are also available in PostgreSQL for applications which don't generally need full transaction isolation and prefer to explicitly manage particular points of conflict. However, proper use of MVCC will generally provide better performance than locks. In addition, application-defined advisory locks provide a mechanism for acquiring locks that are not tied to a single transaction.


Isolation level
---------------

  * Read Committed

Read Committed is the default isolation level in PostgreSQL. When a transaction uses this isolation level, a SELECT query (without a FOR UPDATE/SHARE clause) sees only data committed before the query began; it never sees either uncommitted data or changes committed during query execution by concurrent transactions.
In effect, a SELECT query sees a snapshot of the database as of the instant the query begins to run. However, SELECT does see the effects of previous updates executed within its own transaction, even though they are not yet committed. Also note that two successive SELECT commands can see different data, even though they are within a single transaction, if other transactions commit changes after the first SELECT starts and before the second SELECT starts.


UPDATE, DELETE, SELECT FOR UPDATE, and SELECT FOR SHARE commands behave the same as SELECT in terms of searching for target rows: they will only find target rows that were committed as of the command start time.
However, such a target row might have already been updated (or deleted or locked) by another concurrent transaction by the time it is found.
In this case, the would-be updater will wait for the first updating transaction to commit or roll back (if it is still in progress).
If the first updater rolls back, then its effects are negated and the second updater can proceed with updating the originally found row.
If the first updater commits, the second updater will ignore the row if the first updater deleted it, otherwise it will attempt to apply its operation to the updated version of the row. The search condition of the command (the WHERE clause) is re-evaluated to see if the updated version of the row still matches the search condition. If so, the second updater proceeds with its operation using the updated version of the row. In the case of SELECT FOR UPDATE and SELECT FOR SHARE, this means it is the updated version of the row that is locked and returned to the client.

Because Read Committed mode starts each command with a new snapshot that includes all transactions committed up to that instant, subsequent commands in the same transaction will see the effects of the committed concurrent transaction in any case. The point at issue above is whether or not a single command sees an absolutely consistent view of the database.
