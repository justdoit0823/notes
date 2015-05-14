
#include "binary-tree.h"
#include "stdlib.h"

_binary_tree * new_binary_tree(int size)
{
	int mem_size = sizeof(_binary_node_ptr) * (size - 1) + sizeof(_binary_tree);
	_binary_tree * tree = (_binary_tree *)malloc(mem_size);
	if(tree == NULL){
		print("malloc memory failure.\n");
		return tree;
	}
	tree->node_num = 0;
	tree->total_num = size;
}


int add_binary_tree_node(_binary_tree * tree, _binary_node_ptr node)
{
	if(tree->node_num > tree->total_num){
		print("binary tree memory full.\n");
		return -1;
	}
	tree->node_list[tree->node_num] = node;
	tree->node_num++;
	return 0;
}

int free_binary_tree(_binary_tree * tree)
{
	int start = 0;
	for(;start < tree->node_num; start++){
		free(tree->node_list[start]);
	}
	free(tree);
}
