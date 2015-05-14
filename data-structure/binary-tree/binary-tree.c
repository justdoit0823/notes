
#include "binary-tree.h"
#include "stdlib.h"

_binary_tree * new_binary_tree(int size)
{
  int mem_size = sizeof(_binary_node) * size;
  _binary_tree * tree = (_binary_tree *)malloc(mem_size);
  if(tree == NULL){
    print("malloc memory failure");
    return tree;
  }
  tree->node_num = 0;
  tree->total_num = size;
}


int add_binary_tree_node(_binary_tree * tree, _binary_node * node)
{

}
