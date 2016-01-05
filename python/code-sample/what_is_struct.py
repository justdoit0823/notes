# -*- coding: utf-8 -*-

'''
This py file show how struct works in python.
The format mapping when struct pack and unpack
is like this:
Format      C Type           Python Type          Standard Size
x           padding            no value
c           char           string of lenght 1        1
b           signed char        integer               1
B           unsigned char      integer               1
?           bool               bool                  1
h           short              integer               2
H           unsigned short     integer               2
i           integer            integer               4
I           unsinged integer   integer               4
l           long               integer               4
L           unsinged long      integer               4
q           long long          integer               8
Q           unsigned long long interger              8
f           float              float                 4
d           double             double                8
s           char []            string
p           char []            string
P           void *             integer

----------------------------------------------------------------

byte order mapping is like this:
character   byte order           size               Alignment
@           native               native              native
=           native               standard             none
<           little-endian        standard             none
>           big-endian           standard             none
!           network(big-endian)  standard             none

'''


import struct
import cStringIO

def show_struct():

    inta = 1234
    floatb = 5678.90
    strc = 'hello'
    format = 'if%ds' % len(strc)
    sp = struct.pack(format, inta, floatb, strc)
    print repr(sp)
    print struct.unpack(format, sp)
    buf = cStringIO.StringIO()
    with open('/tmp/testfile', 'w') as f:
        struct.pack_into(format, f, 0, inta, floatb, strc)
        print buf.getvalue()
        print struct.unpack_from(format, buf)
        f.close()


if __name__ == '__main__':


    show_struct()
