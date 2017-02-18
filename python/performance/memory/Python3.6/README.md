
Abstract
========

The dict type has been reimplemented to use a more compact representation based on a proposal by Raymond Hettinger and similar to the PyPy dict implementation.

This resulted in dictionaries using 20% to 25% less memory when compared to Python 3.5.


Implementation
==============

Example
-------

```
For example, the dictionary:

    d = {'timmy': 'red', 'barry': 'green', 'guido': 'blue'}

is currently stored as:

    entries = [['--', '--', '--'],
               [-8522787127447073495, 'barry', 'green'],
               ['--', '--', '--'],
               ['--', '--', '--'],
               ['--', '--', '--'],
               [-9092791511155847987, 'timmy', 'red'],
               ['--', '--', '--'],
               [-6480567542315338377, 'guido', 'blue']]

Instead, the data should be organized as follows:

    indices =  [None, 1, None, None, None, 0, None, 2]
    entries =  [[-9092791511155847987, 'timmy', 'red'],
                [-8522787127447073495, 'barry', 'green'],
                [-6480567542315338377, 'guido', 'blue']]
```


Structure
---------

```
/* See dictobject.c for actual layout of DictKeysObject */
struct _dictkeysobject {
    Py_ssize_t dk_refcnt;

    /* Size of the hash table (dk_indices). It must be a power of 2. */
    Py_ssize_t dk_size;

    /* Function to lookup in the hash table (dk_indices):

       - lookdict(): general-purpose, and may return DKIX_ERROR if (and
         only if) a comparison raises an exception.

       - lookdict_unicode(): specialized to Unicode string keys, comparison of
         which can never raise an exception; that function can never return
         DKIX_ERROR.

       - lookdict_unicode_nodummy(): similar to lookdict_unicode() but further
         specialized for Unicode string keys that cannot be the <dummy> value.

       - lookdict_split(): Version of lookdict() for split tables. */
    dict_lookup_func dk_lookup;

    /* Number of usable entries in dk_entries. */
    Py_ssize_t dk_usable;

    /* Number of used entries in dk_entries. */
    Py_ssize_t dk_nentries;

    /* Actual hash table of dk_size entries. It holds indices in dk_entries,
       or DKIX_EMPTY(-1) or DKIX_DUMMY(-2).

       Indices must be: 0 <= indice < USABLE_FRACTION(dk_size).

       The size in bytes of an indice depends on dk_size:

       - 1 byte if dk_size <= 0xff (char*)
       - 2 bytes if dk_size <= 0xffff (int16_t*)
       - 4 bytes if dk_size <= 0xffffffff (int32_t*)
       - 8 bytes otherwise (int64_t*)

       Dynamically sized, 8 is minimum. */
    union {
        int8_t as_1[8];
        int16_t as_2[4];
        int32_t as_4[2];
#if SIZEOF_VOID_P > 4
        int64_t as_8[1];
#endif
	} dk_indices;

    /* "PyDictKeyEntry dk_entries[dk_usable];" array follows:
       see the DK_ENTRIES() macro */
};
```


Layout
------

```
+---------------+
| dk_refcnt     |
| dk_size       |
| dk_lookup     |
| dk_usable     |
| dk_nentries   |
+---------------+
| dk_indices    |
|               |
+---------------+
| dk_entries    |
|               |
+---------------+
```


Benchmark
===========

Python Size
-------------

Python Version  |  1 | 4  | 10 | 50 | 100 | 500 | 1000 | 5000 | 10000
--------------  | -- | -- | ---|----|-----|-----|----- |------|------
2.7             |280 |280 |1048| 3352| 12568| 49432| 49432| 196888| 786712
3.6             |240 |240 |368 |2280 |4704 |18528 |36968 |147560| 295008



References
==========

  * <https://docs.python.org/3/whatsnew/3.6.html#whatsnew36-compactdict>

  * <https://mail.python.org/pipermail/python-dev/2012-December/123028.html>

  * <https://morepypy.blogspot.com/2015/01/faster-more-memory-efficient-and-more.html>
