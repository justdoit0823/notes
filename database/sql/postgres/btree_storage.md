
Btree
=====

Block
-----

  * itemptr

Itemptr points to the index tuple in the ascending order.

  * index tuple

The tuple includes `ctid` and index data.

  * high key

A specified index tuple, which index data is larger than all the left index tuples within the block.


Index meta
-----------

Getting the index meta data with the following sql,

```
select * from bt_metap('index_name');
```

The field `root` is the index root block.


Root block
----------

```
 itemoffset |   ctid   | itemlen | nulls | vars |          data
------------+----------+---------+-------+------+-------------------------
          1 | (3,1)    |       8 | f     | f    |
          2 | (411,1)  |      16 | f     | f    | 77 97 01 00 00 00 00 00
          3 | (698,1)  |      16 | f     | f    | ed 2e 03 00 00 00 00 00
          4 | (984,1)  |      16 | f     | f    | 63 c6 04 00 00 00 00 00
          5 | (1270,1) |      16 | f     | f    | d9 5d 06 00 00 00 00 00
          6 | (1556,1) |      16 | f     | f    | 4f f5 07 00 00 00 00 00
          7 | (1842,1) |      16 | f     | f    | c5 8c 09 00 00 00 00 00
          8 | (2128,1) |      16 | f     | f    | 3b 24 0b 00 00 00 00 00
          9 | (2414,1) |      16 | f     | f    | b1 bb 0c 00 00 00 00 00
         10 | (2700,1) |      16 | f     | f    | 27 53 0e 00 00 00 00 00
```

The first item has no data. The left items point to non-leaf or leaf blocks.


Non leaf block
--------------

### Non rightmost non-leaf block ###

```
          1 | (574,1) |      16 | f     | f    | ed 2e 03 00 00 00 00 00
          2 | (287,1) |       8 | f     | f    |
          3 | (288,1) |      16 | f     | f    | e5 98 01 00 00 00 00 00
          4 | (289,1) |      16 | f     | f    | 53 9a 01 00 00 00 00 00
          5 | (290,1) |      16 | f     | f    | c1 9b 01 00 00 00 00 00
          6 | (291,1) |      16 | f     | f    | 2f 9d 01 00 00 00 00 00
          7 | (292,1) |      16 | f     | f    | 9d 9e 01 00 00 00 00 00
          8 | (293,1) |      16 | f     | f    | 0b a0 01 00 00 00 00 00
          9 | (294,1) |      16 | f     | f    | 79 a1 01 00 00 00 00 00
         10 | (295,1) |      16 | f     | f    | e7 a2 01 00 00 00 00 00
         11 | (296,1) |      16 | f     | f    | 55 a4 01 00 00 00 00 00
         12 | (297,1) |      16 | f     | f    | c3 a5 01 00 00 00 00 00
         13 | (298,1) |      16 | f     | f    | 31 a7 01 00 00 00 00 00
         14 | (299,1) |      16 | f     | f    | 9f a8 01 00 00 00 00 00
         15 | (300,1) |      16 | f     | f    | 0d aa 01 00 00 00 00 00
         16 | (301,1) |      16 | f     | f    | 7b ab 01 00 00 00 00 00
         17 | (302,1) |      16 | f     | f    | e9 ac 01 00 00 00 00 00
         18 | (303,1) |      16 | f     | f    | 57 ae 01 00 00 00 00 00
```

The first item is the high key. The second item has no data, and all items within the located block are less than the next block item data.


### Rightmost non leaf block ###

```
          1 | (2576,1) |       8 | f     | f    |
          2 | (2577,1) |      16 | f     | f    | 95 54 0e 00 00 00 00 00
          3 | (2578,1) |      16 | f     | f    | 03 56 0e 00 00 00 00 00
          4 | (2579,1) |      16 | f     | f    | 71 57 0e 00 00 00 00 00
          5 | (2580,1) |      16 | f     | f    | df 58 0e 00 00 00 00 00
          6 | (2581,1) |      16 | f     | f    | 4d 5a 0e 00 00 00 00 00
          7 | (2582,1) |      16 | f     | f    | bb 5b 0e 00 00 00 00 00
          8 | (2583,1) |      16 | f     | f    | 29 5d 0e 00 00 00 00 00
          9 | (2584,1) |      16 | f     | f    | 97 5e 0e 00 00 00 00 00
         10 | (2585,1) |      16 | f     | f    | 05 60 0e 00 00 00 00 00
```

The first item has no data, and all items within the located block are larger than the data of the parent block item points to this block.


Leaf block
------------

```
          1 | (463,39)  |      16 | f     | f    | e5 98 01 00 00 00 00 00
          2 | (461,125) |      16 | f     | f    | 77 97 01 00 00 00 00 00
          3 | (461,126) |      16 | f     | f    | 78 97 01 00 00 00 00 00
          4 | (461,127) |      16 | f     | f    | 79 97 01 00 00 00 00 00
          5 | (461,128) |      16 | f     | f    | 7a 97 01 00 00 00 00 00
          6 | (461,129) |      16 | f     | f    | 7b 97 01 00 00 00 00 00
          7 | (461,130) |      16 | f     | f    | 7c 97 01 00 00 00 00 00
          8 | (461,131) |      16 | f     | f    | 7d 97 01 00 00 00 00 00
          9 | (461,132) |      16 | f     | f    | 7e 97 01 00 00 00 00 00
         10 | (461,133) |      16 | f     | f    | 7f 97 01 00 00 00 00 00
```

The first block item is high key. The left block items point to the related relation tuples.



Reference
=========

  * pageinspect
