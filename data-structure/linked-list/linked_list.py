
"""Linked list."""

from collections import deque
import random


class Node:

    def __init__(self, value):
        """Initialize list node."""
        self._val = value
        self._next = None

    def __add__(self, node):
        """Concat two nodes."""
        self._next = node

    @property
    def value(self):
        """Return value of the node."""
        return self._val

    @property
    def next(self):
        """Return the next node."""
        return self._next

    @next.setter
    def next(self, node):
        """Set the next node."""
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


def quick_sort(head_node, tail_node):
    """Quicksort algorithm based on linked list."""

    def partition(s_node, e_node):
        low_tail = None
        low_head = None

        pivot_node = s_node
        pivot_val = pivot_node.value

        prev_node = pivot_node
        cur_node = pivot_node.next
        while cur_node is not None and cur_node is not e_node:
            next_node = cur_node.next

            if cur_node.value < pivot_val:
                if low_tail is None:
                    low_head = cur_node
                    low_tail = low_head
                else:
                    low_tail.next = cur_node
                    low_tail = cur_node

                prev_node.next = next_node
            else:
                prev_node = cur_node

            cur_node = next_node

        if low_head is None:
            low_head = pivot_node
            low_tail = pivot_node
        else:
            low_tail.next = pivot_node

        return low_head, pivot_node

    q = deque()
    ret = None

    while True:
        h_node, p_node = partition(head_node, tail_node)

        if p_node.next is not tail_node:
            q.append((p_node, p_node.next, tail_node))

        if h_node is p_node:
            break

        head_node = h_node
        tail_node = p_node

    ret = h_node

    while q:
        mid_node, head_node, tail_node = q.pop()
        h_node, p_node = partition(head_node, tail_node)

        if h_node is not head_node:
            mid_node.next = h_node

        if h_node is not p_node:
            q.append((mid_node, h_node, p_node))

        if p_node.next is not tail_node and p_node.next is not None:
            q.append((p_node, p_node.next, tail_node))

    return ret


def test_quick_sort(num=100):
    """Test quicksort algorithm."""

    def get_linked_list_data(node):
        cur_node = node
        while cur_node is not None:
            yield cur_node.value
            cur_node = cur_node.next

    for idx in range(num):
        first_node = Node(idx)

        cur_node = first_node
        for idx in range(1000):
            new_node = Node(random.randint(10, 1000))
            cur_node + new_node
            cur_node = new_node

        value_list = tuple(get_linked_list_data(first_node))
        head_node = quick_sort(first_node, None)

        assert tuple(get_linked_list_data(head_node)) == tuple(sorted(value_list))


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

    test_quick_sort()


if __name__ == '__main__':
    main()
