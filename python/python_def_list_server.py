# -*- utf-8 -*-


import ast
import tokenize
from epc.server import EPCServer
from collections import deque





def get_file_def_list(*args):
    filename = args[0]
    with open(filename) as f:
        source = f.read()
    main_node = ast.parse(source)
    node_list = []
    for node in main_node.body:
        node_list.append(parse_def_node(node))
    return list(filter(bool, node_list))


def get_file_def_pos(*args):
    def_list = get_file_def_list(*args)
    def_token = get_file_def_token(args[0])
    return iter_def_list(def_list, def_token)


def iter_def_list(def_list, token_map, rootclass=None):
    def_map = {}
    for d in def_list:
        def_type = d[0]
        if rootclass is None:
            def_map[d[1]] = token_map[d[1]]
        else:
            new_name = rootclass + '.' + d[1]
            def_map[new_name] = token_map[new_name]

        if def_type == 'class':
            # sub def in class
            def_map.update(iter_def_list(d[-1], token_map, d[1]))
    return def_map


def echo(*args):
    return args


def parse_def_node(node):
    if isinstance(node, ast.FunctionDef):
        # function node
        return ('function', node.name, node.lineno, node.col_offset)
    elif isinstance(node, ast.ClassDef):
        # class node
        children_list = []
        for n in node.body:
            children_list.append(parse_def_node(n))
        care_children = tuple(filter(bool, children_list))
        return ('class', node.name, node.lineno, node.col_offset, care_children)
    return ()


def get_file_def_token(filename):
    readline = open(filename).readline
    token_generator = tokenize.generate_tokens(readline)
    care_name_set = frozenset(('def', 'class'))
    token_set1 = frozenset((tokenize.INDENT, tokenize.DEDENT))
    token_set2 = frozenset((tokenize.NAME, tokenize.INDENT, tokenize.DEDENT))
    function_def = False
    class_def = False
    function_indent = False
    class_indent = False
    function_dedent = False
    class_dedent = False
    token_map = {}
    class_queue = deque()
    function_queue = deque()
    class_function_queue = deque()
    class_class_queue = deque()
    root_class_name = ''

    while True:
        try:
            token_type, token_str, start, end, __ = next(token_generator)
        except StopIteration:
            break
        if not class_def:
            # no class defined before

            if not function_def:
                # no function defined before

                if token_type != tokenize.NAME or\
                   token_str not in care_name_set:
                    continue

                if token_str == 'def':
                    # def function block start
                    token_type, token_str, start, end, __ = next(token_generator)
                    if token_type != tokenize.NAME:
                        # irregular defination
                        continue
                    function_def = True
                    token_map[token_str] = start

                if token_str == 'class':
                    # def class block start
                    token_type, token_str, start, end, __ = next(token_generator)
                    if token_type != tokenize.NAME:
                        # irregular defination
                        continue
                    class_def = True
                    class_name = token_str
                    root_class_name = token_str
                    token_map[token_str] = start

            else:
                if token_type not in token_set1:
                    continue

                if token_type == tokenize.INDENT:
                    # indent here
                    if not function_indent:
                        function_indent = True
                    else:
                        function_queue.append(True)
                elif token_type == tokenize.DEDENT and function_indent and\
                     not function_dedent:
                    # dedent here
                    # function_dedent = True
                    try:
                        function_queue.pop()
                    except IndexError:
                        function_indent = False
                        function_def = False
        else:
            # class defined before

            if not function_def:
                # no function defined in class

                if token_type not in token_set2:
                    continue
                if token_type == tokenize.INDENT:
                    # indent here
                    class_indent = True
                elif token_type == tokenize.NAME:
                    if token_str not in care_name_set:
                        continue

                    if token_str == 'def':
                        # def function in class
                        token_type, token_str, start, end, __ = next(
                            token_generator)
                        if token_type != tokenize.NAME:
                            # irregular defination
                            continue
                        function_def = True
                        new_token_key = root_class_name + '.' + token_str
                        token_map[new_token_key] = start

                    if token_str == 'class':
                        # def class in class
                        token_type, token_str, start, end, __ = next(
                            token_generator)
                        if token_type != tokenize.NAME:
                            # irregular defination
                            continue
                        class_def = True
                        class_name = token_str
                        new_token_key = root_class_name + '.' + token_str
                        token_map[new_token_key] = start
                        class_queue.append((root_class_name, class_indent))
                        root_class_name = token_str
                        class_indent = False
                elif token_type == tokenize.DEDENT and class_indent:
                    # dedent here
                    class_dedent = True
                    try:
                        root_class_name, class_indent = class_queue.pop()
                        class_def = True
                    except IndexError:
                        root_class_name = ''
                        class_indent = False
                        class_def = False

            else:
                # function defined in class

                if token_type not in token_set1:
                    continue

                if token_type == tokenize.INDENT:
                    # indent here
                    if not function_indent:
                        function_indent = True
                    else:
                        class_function_queue.append(True)

                elif token_type == tokenize.DEDENT and function_indent:
                    # dedent here
                    # function_dedent = True
                    try:
                        class_function_queue.pop()
                    except IndexError:
                        function_indent = False
                        function_def = False
    return token_map


def main():
    server  = EPCServer(('localhost', 9898))
    server.register_function(echo)
    server.register_function(get_file_def_pos)
    server.print_port()
    server.serve_forever()


if __name__ == '__main__':
    main()
