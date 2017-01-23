
Query Results
=============

String comparison
-----------------

```
mysql> select '1' = 1;
+---------+
| '1' = 1 |
+---------+
|       1 |
+---------+
1 row in set (0.00 sec)

mysql> select '' = 0;
+--------+
| '' = 0 |
+--------+
|      1 |
+--------+
1 row in set (0.00 sec)

mysql> select 's' = 0;
+---------+
| 's' = 0 |
+---------+
|       1 |
+---------+
1 row in set, 1 warning (0.00 sec)

mysql> select 'ssdfwefwefwe' = 0;
+--------------------+
| 'ssdfwefwefwe' = 0 |
+--------------------+
|                  1 |
+--------------------+
1 row in set, 1 warning (0.00 sec)

mysql> select '1ssdfwefwefwe' = 1;
+---------------------+
| '1ssdfwefwefwe' = 1 |
+---------------------+
|                   1 |
+---------------------+
1 row in set, 1 warning (0.00 sec)
```

Emypt string in query
---------------------

```
mysql> select * from s_empty_as_zero;
+------+
| id   |
+------+
|    0 |
|    1 |
+------+
2 rows in set (0.00 sec)

mysql> select * from s_empty_as_zero where id in ('');
+------+
| id   |
+------+
|    0 |
+------+
1 row in set (0.00 sec)

mysql> select * from s_empty_as_zero where id in (0);
+------+
| id   |
+------+
|    0 |
+------+
1 row in set (0.00 sec)

mysql> select * from s_empty_as_zero where id in (1);
+------+
| id   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

Type Conversion
===============

String is implicitly converted to floating-point numbers.

How MySQL handle type conversion
--------------------------------

  * If one or both arguments are NULL, the result of the comparison is NULL, except for the NULL-safe <=> equality comparison operator. For NULL <=> NULL, the result is true. No conversion is needed. 

  * If both arguments in a comparison operation are strings, they are compared as strings. 

  * If both arguments are integers, they are compared as integers. 

  *  Hexadecimal values are treated as binary strings if not compared to a number.

  *  If one of the arguments is a TIMESTAMP or DATETIME column and the other argument is a constant, the constant is converted to a timestamp before the comparison is performed. This is done to be more ODBC-friendly. Note that this is not done for the arguments to IN()! To be safe, always use complete datetime, date, or time strings when doing comparisons. For example, to achieve best results when using BETWEEN with date or time values, use CAST() to explicitly convert the values to the desired data type. A single-row subquery from a table or tables is not considered a constant. For example, if a subquery returns an integer to be compared to a DATETIME value, the comparison is done as two integers. The integer is not converted to a temporal value. To compare the operands as DATETIME values, use CAST() to explicitly convert the subquery value to DATETIME. 

  * If one of the arguments is a decimal value, comparison depends on the other argument. The arguments are compared as decimal values if the other argument is a decimal or integer value, or as floating-point values if the other argument is a floating-point value. 

  * In all other cases, the arguments are compared as floating-point (real) numbers. 


How to check the real number
==============================

```
CREATE FUNCTION `isinteger`(v varchar(255)) RETURNS bit(1)
BEGIN

    RETURN CASE WHEN CONCAT('', v * 1) = v THEN 1 ELSE 0 END;

END
```


Reference
=========

  * <https://dev.mysql.com/doc/refman/5.7/en/type-conversion.html>

  * <http://dba.stackexchange.com/questions/89760/prevent-mysql-from-mangling-queries-by-casting-string-to-int>
