
What Is Binary Log
==================

A file containing a record of all statements that attempt to change table data.

These statements can be replayed to bring slave servers up to date in a replication scenario,

or to bring a database up to date after restoring table data from a backup.

The binary logging feature can be turned on and off, although Oracle recommends always enabling it if you use replication or perform backups. 

**Note: different from redo log.**


How To Enable
=============

To enable the binary log, start the server with the --log-bin[=base\_name] option.

If no base_name value is given, the default name is the value of the pid-file option (which by default is the name of host machine) followed by -bin.

If the base name is given, the server writes the file in the data directory unless the base name is given with a leading absolute path name to specify a different directory.


How To Inspect
==============

SQL Command
-----------

  * show binary logs

```
+-----------+-----------+
| Log_name  | File_size |
+-----------+-----------+
| on.000001 |       786 |
| on.000002 |       457 |
+-----------+-----------+
```

Lists the binary log files on the server.


  * show binlog events

```
+-----------+-----+----------------+-----------+-------------+----------------------------------------------+
| Log_name  | Pos | Event_type     | Server_id | End_log_pos | Info                                         |
+-----------+-----+----------------+-----------+-------------+----------------------------------------------+
| on.000002 |   4 | Format_desc    |         1 |         123 | Server ver: 5.7.13-log, Binlog ver: 4        |
| on.000002 | 123 | Previous_gtids |         1 |         154 |                                              |
| on.000002 | 154 | Anonymous_Gtid |         1 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'         |
| on.000002 | 219 | Query          |         1 |         296 | BEGIN                                        |
| on.000002 | 296 | Table_map      |         1 |         364 | table_id: 263 (workspace.tbl_test_partition) |
| on.000002 | 364 | Update_rows    |         1 |         426 | table_id: 263 flags: STMT_END_F              |
| on.000002 | 426 | Xid            |         1 |         457 | COMMIT /* xid=291 */                         |
+-----------+-----+----------------+-----------+-------------+----------------------------------------------+
```

Shows the events in the binary log.


mysqlbinlog
-----------

Dumps a MySQL binary log in a format usable for viewing or for piping to
the mysql command line client.

```
BEGIN
/*!*/;
# at 296
#170316 12:45:03 server id 1  end_log_pos 364 CRC32 0xde4cc87f  Table_map: `workspace`.`tbl_test_partition` mapped to number 263
# at 364
#170316 12:45:03 server id 1  end_log_pos 426 CRC32 0xb629aa70  Update_rows: table id 263 flags: STMT_END_F

BINLOG '
TxjKWBMBAAAARAAAAGwBAAAAAAcBAAAAAAEACXdvcmtzcGFjZQASdGJsX3Rlc3RfcGFydGl0aW9u
AAMDAwMABn/ITN4=
TxjKWB8BAAAAPgAAAKoBAAAAAAcBAAAAAAEAAgAD///4AgAAAOgDAAAYMAAA+AIAAADoAwAAAQAA
AHCqKbY=
'/*!*/;
### UPDATE `workspace`.`tbl_test_partition`
### WHERE
###   @1=2 /* INT meta=0 nullable=0 is_null=0 */
###   @2=1000 /* INT meta=0 nullable=1 is_null=0 */
###   @3=12312 /* INT meta=0 nullable=1 is_null=0 */
### SET
###   @1=2 /* INT meta=0 nullable=0 is_null=0 */
###   @2=1000 /* INT meta=0 nullable=1 is_null=0 */
###   @3=1 /* INT meta=0 nullable=1 is_null=0 */
# at 426
#170316 12:45:03 server id 1  end_log_pos 457 CRC32 0xd827f3d3  Xid = 291
COMMIT/*!*/;
```

  * --base64-output

Determine when the output statements should be base64-encoded BINLOG statements:

'never' disables it and works only for binlogs without row-based events;

'decode-rows' decodes row events into commented pseudo-SQL statements if the --verbose option is also given;

'auto' prints base64 only when necessary (i.e., for row-based events and format description events).

If no --base64-output[=name] option is given at all, the default is 'auto'.


  * --verbose

Reconstruct pseudo-SQL statements out of row events. -vv adds comments on column data types.


Reference
=========

  * <https://dev.mysql.com/doc/refman/5.6/en/glossary.html#glos_binary_log>

  * <https://dev.mysql.com/doc/refman/5.6/en/binary-log.html>

  * <https://www.percona.com/blog/2015/07/30/why-base64-outputdecode-rows-does-not-print-row-events-in-mysql-binary-logs/>
