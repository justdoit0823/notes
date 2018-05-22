
"""Binary search tree."""

from collections import deque
import random

from graphviz import Digraph


class Node:

    def __init__(self, val):
        self._val = val
        self._left = None
        self._right = None

    def __str__(self):
        return 'node-%d' % id(self)

    @property
    def value(self):
        return self._val

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node


class BinarySearchTree:

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    def insert(self, val):
        parent_node, matched_node, __ = self._search(val)
        if matched_node is not None:
            raise ValueError('Node %d already exists.' % val)

        if parent_node is None:
            self._root = Node(val)
        else:
            if val < parent_node.value:
                parent_node.left = Node(val)
            else:
                parent_node.right = Node(val)

    def delete(self, val):
        parent_node, matched_node, direction = self._search(val)
        print(parent_node.value, matched_node.value, direction)
        self._adjust_right(parent_node, matched_node, direction)

    def search(self, val):
        __, matched_node, __ = self._search(val)
        return matched_node

    def _search(self, val):
        prev_node = None
        cur_node = self._root
        direction = 0

        while cur_node is not None:
            node_val = cur_node.value
            if node_val == val:
                break

            if val < node_val:
                prev_node = cur_node
                cur_node = cur_node.left
            else:
                prev_node = cur_node
                cur_node = cur_node.right

        if cur_node is not None and prev_node is not None:
            if cur_node is prev_node.left:
                direction = 1
            else:
                direction = 2

        return prev_node, cur_node, direction

    def _adjust_right(self, parent_node, matched_node, direction):
        prev_node = parent_node
        cur_node = matched_node
        next_node = matched_node.right

        # Find the minimum value larger than the matched node's value
        while next_node is not None:
            prev_node = cur_node
            cur_node = next_node
            next_node = next_node.left

        if cur_node is not matched_node:
            cur_node_right = cur_node.right

            cur_node.left = matched_node.left

            if cur_node is not matched_node.right:
                cur_node.right = matched_node.right

            if prev_node is not matched_node:
                prev_node.left = cur_node_right
        else:
            # no right sub-node
            cur_node = cur_node.left

        if direction == 0:
            self._root = cur_node
        elif direction == 1:
            parent_node.left = cur_node
        else:
            parent_node.right = cur_node

    def show(self, filename=None, cleanup=False):
        dot1 = Digraph(comment='Binary search tree')
        queue1 = deque()
        queue1.append((None, self.root))

        while queue1:
            parent_node, cur_node = queue1.popleft()
            dot1.node(str(cur_node), str(cur_node.value))
            if parent_node is not None:
                dot1.edge(str(parent_node), str(cur_node))

            left_node = cur_node.left
            if left_node is not None:
                queue1.append((cur_node, left_node))

            right_node = cur_node.right
            if right_node is not None:
                queue1.append((cur_node, right_node))

        dot1.view(filename=filename, cleanup=cleanup)


def main():
    bst1 = BinarySearchTree()
    values = []

    for idx in range(100):
        val = random.randint(10, 300)
        try:
            bst1.insert(val)
        except ValueError:
            continue
        else:
            values.append(val)

    bst1.show(filename='bst1')

    del_val = random.choice(values)
    print('delete value', del_val)
    bst1.delete(del_val)

    bst1.show(filename='bst1-new')


if __name__ == '__main__':
    main()
