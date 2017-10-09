
"""Disk io benchmark."""

import os
import sys
import tempfile


TOTAL_SIZE = 10 * 1024 * 1024 * 1024


def write_file(page_size, sync=False, last_sync=False):
    path = tempfile.mktemp(prefix='disk-io-py')
    data = b'1' * page_size
    flags = os.O_CREAT|os.O_WRONLY
    if sync:
        flags |= os.O_SYNC

    fd = os.open(path, flags, 644)
    write_bytes = 0
    for i in range(TOTAL_SIZE // page_size):
        write_bytes += os.write(fd, data)

    if last_sync:
        os.fsync(fd)

    print('successfully write %d bytes.' % write_bytes)


def write_buffer_file(page_size, last_sync=False):
    path = tempfile.mktemp(prefix='disk-io-py')
    data = '1' * page_size
    write_bytes = 0

    with open(path, 'x') as f:
        for i in range(TOTAL_SIZE // page_size):
            write_bytes += f.write(data)

        if last_sync:
            f.flush()

    print('successfully write %d bytes.' % write_bytes)


def main():
    if len(sys.argv) < 3:
        print('write method(posix or buffer) and page size are needed.\n')
        return

    method = sys.argv[1]
    page_size = int(sys.argv[2])

    sync = False
    if len(sys.argv) > 3:
        sync = bool(int(sys.argv[3]))

    last_sync = False
    if len(sys.argv) > 4:
        last_sync = bool(int(sys.argv[4]))

    if method == 'posix':
        write_file(page_size, sync=sync, last_sync=last_sync)
    elif method == 'buffer':
        write_buffer_file(page_size, last_sync=last_sync)
    else:
        print('invalid writing method.\n')


if __name__ == '__main__':
    main()
