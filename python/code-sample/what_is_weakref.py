# -*- coding: utf-8 -*-

'''
This module shows how weakref works.
See details at https://docs.python.org/2/library/weakref.html

'''


import weakref
import sys


class WeakrefDict(dict):
    '''
    A weakref dictionary
    '''
    pass


class NotWeakableClass:

    def __init__(self, v):
        self._v = v


def show_weakref():

    d = {'color': 'blue', 'value': 512, 'weight': 64}
    wd = WeakrefDict({'color': 'red', 'value': 255, 'weight': 128})
    nwc = NotWeakableClass(12345)
    print(d, sys.getrefcount(d))
    print(wd, weakref.getweakrefcount(wd))
    try:
        dref = weakref.ref(d)
    except Exception as e:
        print('create weakref error:', e)
    else:
        print(dref, dref(), weakref.getweakrefcount(dref()))
    try:
        nwcref = weakref.ref(nwc)
    except Exception as e:
        print('create weakref error:', e)
    else:
        print(nwcref, nwcref(), weakref.getweakrefcount(nwcref()))
    try:
        NotWC = weakref.ref(NotWeakableClass)
    except Exception as e:
        print('create weakref error:', e)
    else:
        print(NotWC, NotWC(), weakref.getweakrefcount(NotWC()))
    wdref = weakref.ref(wd)
    print(wdref, wdref(), weakref.getweakrefcount(wdref()))
    del wd
    print(wdref())
    # weakref value dictionary
    wvd = weakref.WeakValueDictionary()
    x = WeakrefDict({'width': 1366, 'height': 768})
    print(wvd, x)
    xid = id(x)
    wvd[xid] = x
    print(wvd[xid])
    # weakref key dictionary
    wkd = weakref.WeakKeyDictionary()
    wkd[nwc] = xid
    del xid
    print(wkd[nwc])
    del nwc
    print([v for v in wkd.values()])
