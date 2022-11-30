from pathlib import Path
from collections import defaultdict
from copy import copy

# input_path = Path(f'{__file__}/../input_example.txt').resolve()
# input_path = Path(f'{__file__}/../input_example2.txt').resolve()
# input_path = Path(f'{__file__}/../input_example3.txt').resolve()
input_path = Path(f'{__file__}/../input_chris.txt').resolve()

print(input_path)

with open(input_path) as f:
    input_text = f.readlines()

in_lines = [line.strip('\n') for line in input_text]

print(in_lines)

nodes = defaultdict(set)

for line in in_lines:
    n0, n1 = line.split('-')
    nodes[n0].add(n1)
    nodes[n1].add(n0)

print(nodes)

end_node = 'end'
start_node = 'start'
node_paths = None
new_node_paths = [([start_node], 0)]

while new_node_paths != node_paths:
    node_paths = copy(new_node_paths)
    new_node_paths = []
    for node_path, extra_visit in node_paths:
        path_end = node_path[-1]
        if path_end == end_node:
            new_node_paths.append((node_path, extra_visit))
            continue
        else:
            for child in nodes[path_end]:
                if child == start_node:
                    continue
                if (child.islower()
                    and (child in set(node_path))):
                    if not extra_visit:
                        new_node_paths.append((node_path+[child], 1))
                    continue
        
                new_node_paths.append((node_path+[child], extra_visit))
print(len(new_node_paths))
