
"""Disk io benchmark."""

import os
import sys
import tempfile


def write_file(total_size, page_size, sync=False, last_sync=False):
    path = tempfile.mktemp(prefix='disk-io-py', dir='/tmp')
    data = b'1' * page_size
    flags = os.O_CREAT|os.O_WRONLY
    if sync:
        flags |= os.O_SYNC

    fd = os.open(path, flags, 644)
    write_bytes = 0
    for i in range(total_size // page_size):
        write_bytes += os.write(fd, data)

    if last_sync:
        os.fsync(fd)

    print('successfully write %d bytes.' % write_bytes)


def main():
    if len(sys.argv) < 3:
        print('total size and page size are needed.\n')
        return

    total_size = int(sys.argv[1])
    page_size = int(sys.argv[2])

    sync = False
    if len(sys.argv) > 3:
        sync = bool(int(sys.argv[3]))

    last_sync = False
    if len(sys.argv) > 4:
        last_sync = bool(int(sys.argv[4]))

    write_file(total_size, page_size, sync=sync, last_sync=last_sync)


if __name__ == '__main__':
    main()
