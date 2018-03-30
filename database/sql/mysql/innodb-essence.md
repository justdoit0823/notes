
InnoDB
=======

`InnoDB` is a general-purpose storage engine that balances high reliability and high performance.
In MySQL 5.7, `InnoDB` is the default MySQL storage engine. Unless you have configured a different default storage engine,
issuing a `CREATE TABLE` statement without an `ENGINE=` clause creates an `InnoDB` table. 


Advantages
----------

  * ACID

Its DML operations follow the ACID model, with transactions featuring commit, rollback, and crash-recovery capabilities to protect user data.


  * MVCC

Row-level locking and Oracle-style consistent reads increase multi-user concurrency and performance.


  * Primary Key

`InnoDB` tables arrange your data on disk to optimize queries based on primary keys.
Each `InnoDB` table has a primary key index called the clustered index that organizes the data to minimize I/O for primary key lookups.


  * Integrity


To maintain data integrity, InnoDB supports FOREIGN KEY constraints.


Architecture
------------

### Buffer Pool ###

The buffer pool is an area in main memory where InnoDB caches table and index data as data is accessed.
The buffer pool allows frequently used data to be processed directly from memory, which speeds up processing.
On dedicated database servers, up to 80% of physical memory is often assigned to the InnoDB buffer pool.

For efficiency of high-volume read operations, the buffer pool is divided into pages that can potentially hold multiple rows.
For efficiency of cache management, the buffer pool is implemented as a linked list of pages; data that is rarely used is aged out of the cache, using a variation of the LRU algorithm.

### Change Buffer ###

The change buffer is a special data structure that caches changes to secondary index pages when affected pages are not in the buffer pool. The buffered changes, which may result from INSERT, UPDATE, or DELETE operations (DML), are merged later when the pages are loaded into the buffer pool by other read operations.

Unlike clustered indexes, secondary indexes are usually nonunique, and inserts into secondary indexes happen in a relatively random order. Similarly, deletes and updates may affect secondary index pages that are not adjacently located in an index tree. Merging cached changes at a later time, when affected pages are read into the buffer pool by other operations, avoids substantial random access I/O that would be required to read-in secondary index pages from disk.

Periodically, the purge operation that runs when the system is mostly idle, or during a slow shutdown, writes the updated index pages to disk. The purge operation can write disk blocks for a series of index values more efficiently than if each value were written to disk immediately.

In memory, the change buffer occupies part of the InnoDB buffer pool. On disk, the change buffer is part of the system tablespace, so that index changes remain buffered across database restarts.


### Adaptive Hash Index ###

The adaptive hash index (AHI) lets InnoDB perform more like an in-memory database on systems with appropriate combinations of workload and ample memory for the buffer pool, without sacrificing any transactional features or reliability.

Based on the observed pattern of searches, MySQL builds a hash index using a prefix of the index key. The prefix of the key can be any length, and it may be that only some of the values in the B-tree appear in the hash index. Hash indexes are built on demand for those pages of the index that are often accessed.

If a table fits almost entirely in main memory, a hash index can speed up queries by enabling direct lookup of any element, turning the index value into a sort of pointer. InnoDB has a mechanism that monitors index searches. If InnoDB notices that queries could benefit from building a hash index, it does so automatically.

The hash index is always built based on an existing B-tree index on the table. InnoDB can build a hash index on a prefix of any length of the key defined for the B-tree, depending on the pattern of searches that InnoDB observes for the B-tree index. A hash index can be partial, covering only those pages of the index that are often accessed.


Read more detail at [adaptive hash index](https://dev.mysql.com/doc/refman/5.7/en/innodb-adaptive-hash.html).


### Redo Log Buffer ###


The redo log buffer is the memory area that holds data to be written to the redo log. Redo log buffer size is defined by the innodb_log_buffer_size configuration option. The redo log buffer is periodically flushed to the log file on disk. A large redo log buffer enables large transactions to run without the need to write redo log to disk before the transactions commit. Thus, if you have transactions that update, insert, or delete many rows, making the log buffer larger saves disk I/O.

The innodb\_flush\_log\_at\_trx\_commit option controls how the contents of the redo log buffer are written to the log file. The innodb\_flush\_log\_at_timeout option controls redo log flushing frequency.


### System Tablespace ###

The InnoDB system tablespace contains the InnoDB data dictionary (metadata for InnoDB-related objects) and is the storage area for the doublewrite buffer, the change buffer, and undo logs. The system tablespace also contains table and index data for any user-created tables that are created in the system tablespace. The system tablespace is considered a shared tablespace since it is shared by multiple tables.

The system tablespace is represented by one or more data files. By default, one system data file, named ibdata1, is created in the MySQL data directory. The size and number of system data files is controlled by the innodb\_data\_file_path startup option.


### Data Directory ###

The InnoDB data dictionary is comprised of internal system tables that contain metadata used to keep track of objects such as tables, indexes, and table columns. The metadata is physically located in the InnoDB system tablespace. For historical reasons, data dictionary metadata overlaps to some degree with information stored in InnoDB table metadata files (.frm files).


### Doublewrite Buffer ###

The doublewrite buffer is a storage area located in the system tablespace where InnoDB writes pages that are flushed from the InnoDB buffer pool, before the pages are written to their proper positions in the data file. Only after flushing and writing pages to the doublewrite buffer, does InnoDB write pages to their proper positions. If there is an operating system, storage subsystem, or mysqld process crash in the middle of a page write, InnoDB can later find a good copy of the page from the doublewrite buffer during crash recovery.

Although data is always written twice, the doublewrite buffer does not require twice as much I/O overhead or twice as many I/O operations. Data is written to the doublewrite buffer itself as a large sequential chunk, with a single fsync() call to the operating system.


### Undo Logs ###

An undo log is a collection of undo log records associated with a single transaction. An undo log record contains information about how to undo the latest change by a transaction to a clustered index record. If another transaction needs to see the original data (as part of a consistent read operation), the unmodified data is retrieved from the undo log records. Undo logs exist within undo log segments, which are contained within rollback segments. Rollback segments reside in the system tablespace, temporary tablespace, and undo tablespaces.

InnoDB supports 128 rollback segments, 32 of which are reserved as non-redo rollback segments for temporary table transactions. Each transaction that updates a temporary table (excluding read-only transactions) is assigned two rollback segments, one redo-enabled rollback segment and one non-redo rollback segment. Read-only transactions are only assigned non-redo rollback segments, as read-only transactions are only permitted to modify temporary tables.


### File-Per-Table Tablespaces ###

A file-per-table tablespace is a single-table tablespace that is created in its own data file rather than in the system tablespace. Tables are created in file-per-table tablespaces when the innodb\_file\_per_table option is enabled. Otherwise, InnoDB tables are created in the system tablespace. Each file-per-table tablespace is represented by a single .ibd data file, which is created in the database directory by default.


### General Tablespaces ###


A shared InnoDB tablespace created using CREATE TABLESPACE syntax. General tablespaces can be created outside of the MySQL data directory, are capable of holding multiple tables, and support tables of all row formats.


### Undo Tablespace ###

An undo tablespace comprises one or more files that contain undo logs. The number of undo tablespaces used by InnoDB is defined by the innodb\_undo_tablespaces configuration option.


### Temporary Tablespace ###

The temporary tablespace is removed on normal shutdown or on an aborted initialization, and is recreated each time the server is started. The temporary tablespace receives a dynamically generated space ID when it is created. Startup is refused if the temporary tablespace cannot be created. The temporary tablespace is not removed if the server halts unexpectedly.


### Redo Log ###

The redo log is a disk-based data structure used during crash recovery to correct data written by incomplete transactions. During normal operations, the redo log encodes requests to change InnoDB table data that result from SQL statements or low-level API calls. Modifications that did not finish updating the data files before an unexpected shutdown are replayed automatically during initialization, and before the connections are accepted.

By default, the redo log is physically represented on disk as a set of files, named ib\_logfile0 and ib_logfile1. MySQL writes to the redo log files in a circular fashion. Data in the redo log is encoded in terms of records affected; this data is collectively referred to as redo. The passage of data through the redo log is represented by an ever-increasing LSN value.


ACID
----

### Atomicity ###

  * Autocommit setting.

  * COMMIT statement.

  * ROLLBACK statement.

  * Operational data from the INFORMATION_SCHEMA tables.


### Consistency ###


  * doublewriter buffer

  * crash recovery


### Isolation ###


  * Autocommit setting.

  * SET ISOLATION LEVEL statement.

  * The low-level details of InnoDB locking.


### Durability ###


  * doublewrite buffer

  * option innodb\_flush\_log\_at\_trx_commit

  * option sync_binlog

  * option innodb\_file\_per_table

  * Write buffer in a storage device, such as a disk drive, SSD, or RAID array.

  * Battery-backed cache in a storage device.

  * fsync system call

  * UPS(Uninterruptible power supply)

  * backup strategy
