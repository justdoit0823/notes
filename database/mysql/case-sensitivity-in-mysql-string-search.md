
String Comparison
=================

  * nonbinary strings

Comparisons use the collation of the comparison operands.


  * binary strings


Comparisons use the numeric values of the bytes in the operands.


  * nonbinary string and binary string

Comparisons are treated as a comparison of binary strings.


Comparison Mechanism
====================

Simple comparison operations (>=, >, =, <, <=, sorting, and grouping) are based on each character's “sort value.”

Characters with the same sort value are treated as the same character


Comparison Result
=================

```
mysql> select 'a' = 'A';
+-----------+
| 'a' = 'A' |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)

mysql> select 'a' collate utf8\_general_ci = 'A' collate utf8_general_ci;
+-----------------------------------------------------------+
| 'a' collate utf8_general_ci = 'A' collate utf8_general_ci |
+-----------------------------------------------------------+
|                                                         1 |
+-----------------------------------------------------------+
1 row in set (0.00 sec)

mysql> select 'a' collate utf8_bin = 'A' collate utf8_bin;
+---------------------------------------------+
| 'a' collate utf8_bin = 'A' collate utf8_bin |
+---------------------------------------------+
|                                           0 |
+---------------------------------------------+
1 row in set (0.00 sec)
```


Comparison Note
===============

  * specify database, table or column collation

  * specify variable collation while comparing


Reference
=========

  * <https://dev.mysql.com/doc/refman/5.6/en/case-sensitivity.html>
