from os import listdir
from os.path import isfile, join, exists
import re
import sys
import matplotlib.pyplot as plt
import networkx as nx

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('wrong number of arguments (!=1)')
        sys.exit(0)

    my_path = sys.argv[1]

    if exists(my_path):
        print('path exists')
    else:
        print('path does not exist')
        sys.exit(1)

    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    py_files = []
    for f in only_files:
        if f.endswith('.py'):
            py_files.append(f)

    print(str(py_files))

    call_dict = {}
    call_list = []

    exclude_file_list = ['experiments.py']

    exclude_list = ['__str__', 'str',
                    'list', 'int', 'assert',
                    'print', 'format', 'join',
                    'open', 'append', 'close',
                    'range', 'info', ]
    'debug'
    include_list = []

    for f in py_files:
        fl = open(my_path + "/" + f, 'r')

        curr_def = ''

        content = fl.read()
        func_defs = re.findall(r'(def\s)([A-z]\w*)(\([A-z0-9=,.-_ ]*\):)', content)
        for fd in func_defs:
            if fd[1] not in include_list:
                include_list.append(fd[1])

        fl.close()

    for e in exclude_list:
        while e in include_list:
            include_list.remove(e)

    print('including: ' + str(include_list))
    print('excluding: ' + str(exclude_list))

    for f in py_files:
        if f not in exclude_file_list:
            fl = open(my_path + "/" + f, 'r')

            curr_def = ''
            curr_class = ''

            content = fl.readlines()
            for l in content:
                class_def = re.findall(r'(class\s)([A-Z]\w*)(\(\w*\):)', l)
                if class_def:
                    curr_class = class_def[0][1]

                func_def = re.findall(r'(def\s)([A-z]\w*)(\([A-z0-9=,.-_ ]*\):)', l)
                if func_def:
                    if func_def[0][1] == '__init__':
                        curr_def = curr_class + '.__init__'

                    elif func_def[0][1] in include_list:
                        curr_def = func_def[0][1]
                else:
                    func_calls = re.findall(r'([a-z]\w*)(\([A-z0-9=,. *\/\(\)]*\))', l)
                    for c in func_calls:
                        if c[0] in include_list and curr_def != '':
                            call_dict[curr_def] = c[0]
                            call_list += [(curr_def, c[0])]

            fl.close()

    print(str(call_dict))

    G = nx.DiGraph(directed=True)

    G.add_edges_from(call_list)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, edge_color='b', arrowsize=20, arrowstyle='fancy')
    plt.show()

    plt.show()
