
"""Cycle linked list."""

import random


class Node:

    def __init__(self, value):
        self._next = None
        self._val = value

    def __add__(self, node):
        """Concat two nodes."""
        self._next = node

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, node):
        self._next = node

    def check_cycle(self):
        slow_ptr = self
        fast_ptr = self
        while slow_ptr is not None and fast_ptr is not None:
            slow_ptr = slow_ptr.next
            if fast_ptr.next is not None:
                fast_ptr = fast_ptr.next.next

            if slow_ptr == fast_ptr:
                return True

        return False

    def cycle_length(self):
        slow_ptr = self
        fast_ptr = self
        start = False
        length = 0
        while slow_ptr is not None and fast_ptr is not None:
            slow_ptr = slow_ptr.next
            if not start and fast_ptr.next is not None:
                fast_ptr = fast_ptr.next.next

            if slow_ptr == fast_ptr:
                if not start:
                    start = True
                else:
                    return length + 1

            if start:
                length += 1

        return 0


def main():
    first_node = Node(0)

    cur_node = first_node
    node_list = [cur_node]
    for idx in range(1, 10):
        node = Node(random.randint(1, 100))
        cur_node + node
        cur_node = node
        node_list.append(cur_node)

    node_idx = random.randint(0, len(node_list) - 1)
    node_list[-1].next = node_list[node_idx]

    assert first_node.check_cycle()
    print('cycle list.')

    c_len = first_node.cycle_length()
    assert c_len == len(node_list) - node_idx + 1
    print('cycle list length', c_len)


if __name__ == '__main__':
    main()
