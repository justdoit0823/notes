
"""Linked list."""

import random


class Node:

    def __init__(self, value):
        """Initialize list node."""
        self._val = value
        self._next = None

    def __add__(self, node):
        """Concat two nodes."""
        self._next = node

    def traverse(self):
        """Traverse the node list."""
        cur_node = self
        while cur_node is not None:
            print(cur_node._val)
            cur_node = cur_node._next

    def search(self, val):
        """Search the first node which equals to input value."""
        eq_node = None
        cur_node = self
        while cur_node is not None:
            if cur_node._val == val:
                eq_node = cur_node
                break

            cur_node = cur_node._next

        return eq_node

    def reverse(self):
        """Reverse the node list."""
        prev_node = None
        cur_node = self
        while cur_node is not None:
            next_node = cur_node._next
            cur_node._next = prev_node
            prev_node = cur_node
            cur_node = next_node

        return prev_node


def main():
    first_node = Node(-123456789)
    val_list = tuple(
        random.randint(1, 9) * 10 ** idx + random.randint(1, 9)
        for idx in range(0, 10))
    print(val_list)

    cur_node = first_node
    for val in val_list:
        new_node = Node(val)
        cur_node + new_node
        cur_node = new_node

    first_node.traverse()

    reversed_node = first_node.reverse()
    reversed_node.traverse()


if __name__ == '__main__':
    main()
