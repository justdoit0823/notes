
"""Binary tree module."""

from collections import deque
import random


class Node:
    """Binary tree node."""

    def __init__(self, val=None):
        self._val = val
        self._left = None
        self._right = None

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, val):
        self._val = val

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        if not isinstance(node, Node):
            raise TypeError('invalid node tyoe.')

        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        if not isinstance(node, Node):
            raise TypeError('invalid node type.')

        self._right = node

    def traverse(self):
        """Traverse the binary tree preorder."""
        print(self.value)

        left_node = self.left
        if left_node is not None:
            left_node.traverse()

        right_node = self.right
        if right_node is not None:
            right_node.traverse()

    def inorder_traverse(self):
        """Traverse the binary tree in order."""
        queue = deque()
        queue.append((self, True))

        while queue:
            node, recursive = queue.pop()
            if not recursive:
                print(node.value)
                continue

            while node is not None:
                right_node = node.right
                if right_node:
                    queue.append((right_node, True))

                queue.append((node, False))
                node = node.left

    def postorder_traverse(self):
        """Traverse the binary tree postorder."""
        queue = deque()
        queue.append((self, True))

        while queue:
            node, recursive = queue.pop()
            if not recursive:
                print(node.value)
                continue

            while node is not None:
                queue.append((node, False))
                right_node = node.right
                if right_node:
                    queue.append((right_node, True))

                node = node.left

    def bfs_traverse(self):
        """Traverse the binary tree bfs."""
        child_nodes = [[self]]
        val_list = []

        while True:
            parent_nodes = child_nodes[-1]
            if not any(parent_nodes):
                break

            child_nodes.append([])
            val_list.append([])

            for node in parent_nodes:
                if node is None:
                    val_list[-1].append('null')
                    child_nodes[-1].append(None)
                    child_nodes[-1].append(None)
                else:
                    val_list[-1].append(node.value)
                    child_nodes[-1].append(node.left)
                    child_nodes[-1].append(node.right)

        level_num = len(val_list)
        for idx, level_val in enumerate(val_list):
            print(' ' * 2 ** (level_num - idx + 1) + (
                ' ' * 2 ** (level_num - idx + 2)).join(map(str, level_val)))


def main():
    level = random.randint(1, 5)
    val_list = tuple(random.randint(1, 100) for idx in range(2 ** level - 1))
    print(val_list)

    parent_nodes = []
    val_idx = 0
    p_idx = None
    while val_idx < len(val_list):
        if p_idx is None:
            new_node = Node(val_list[val_idx])
            parent_nodes.append([new_node])
            val_idx += 1
            p_idx = 0
            continue

        parent_nodes.append([])
        for p_node in parent_nodes[p_idx]:
            new_node = Node(val_list[val_idx])
            p_node.left = new_node
            parent_nodes[-1].append(new_node)

            val_idx += 1

            new_node = Node(val_list[val_idx])
            p_node.right = new_node
            parent_nodes[-1].append(new_node)
            val_idx += 1

        p_idx += 1

    root_node = parent_nodes[0][0]

    print('Preorder traverse...')
    root_node.traverse()

    print('BFS traverse...')
    root_node.bfs_traverse()

    print('Inorder traverse...')
    root_node.inorder_traverse()

    print('Postorder traverse...')
    root_node.postorder_traverse()


if __name__ == '__main__':
    main()
