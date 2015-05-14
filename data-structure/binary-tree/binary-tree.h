
#ifndef _BINARY_TREE_H

typedef int _binary_item_type;

typedef struct {
  _binary_item_type item;
} _binary_node;

typedef _binary_node * _binary_node_ptr;

typedef struct {
  int node_num;
  int total_num;
  _binary_ptr node_list[0];
} _binary_tree;

static _binary_tree * tree_head = NULL;

_binary_tree * new_binary_tree(int size);

int add_binary_tree_node(_binary_tree * tree, _binary_node_ptr node);

int free_binary_tree(_binary_tree * tree);


#endif
