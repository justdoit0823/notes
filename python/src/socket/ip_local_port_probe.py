
"""Ip local port probe.

For test, we should edit the `ip_local_port_range` configuration on your linux machine.

`echo '60909 60999' > /proc/sys/net/ipv4/ip_local_port_range`

Then, run this script with a local server.

"""

import socket
import sys


def probe_local_ports(addr, max_num):
    """Probe the maximum port num."""
    suc_list = []
    for idx in range(max_num):
        c_sock = socket.socket()
        try:
            c_sock.connect(addr)
        except Exception as e:
            print(e)
            break
        else:
            # Refer to the client socket for preventing socket close
            suc_list.append((c_sock, c_sock.getsockname()))

    print('%d connections succeed with %d attempts.\n' % (len(suc_list), max_num))


def main():
    if len(sys.argv) < 2:
        print('Argument addr is needed.')

    addr = sys.argv[1].split(':')
    addr = (addr[0], int(addr[1]))
    max_num = 1000
    if len(sys.argv) > 2:
        max_num = int(sys.argv[2])

    probe_local_ports(addr, max_num)


if __name__ == '__main__':
    main()
