import collections
import sys
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
parser.add_argument('--time', '-t', action='store_true')
args = parser.parse_args()

input_file = args.input  # proj001.input.txt
output_file = args.output  # proj001.output.txt

graph = collections.defaultdict(list)
output = []
with open(input_file) as f:
    for line in f.readlines():
        line_list = line.strip().split(',')
        line_list = list(map(lambda x: x.strip(), line_list))
        if line_list[0] == 'Add':
            start_time = time.perf_counter()
            _, subj, obj, priv = line_list
            if not graph[obj]:
                graph[obj] = [set(), None]
            if not graph[subj]:
                graph[subj] = [set(), set()]
            if priv == 'R':  # obj -> subj
                graph[obj][0].add(subj)  # add outward edge for obj
                graph[subj][1].add(obj)  # add inward edge for subj
            elif priv == 'W':  # subj -> obj
                graph[subj][0].add(obj)  # add outward edge for subj
            else:
                for nei in graph[subj][0]:
                    graph[obj][0].add(nei)  # propagate write priv
                for nei in graph[subj][1]:
                    graph[obj][1].add(nei)  # propagate read priv
                    graph[nei][0].add(obj)
            output.append(','.join(line_list))
            end_time = time.perf_counter()
            if args.time:
                print(f'{line.strip()}: {end_time - start_time}s')
        elif line_list[0] == 'Query':
            start_time = time.perf_counter()
            _, subj, obj, priv = line_list
            if priv == 'R':
                if subj in graph[obj][0]:
                    output.append(','.join(line_list) + ' YES')
                else:
                    output.append(','.join(line_list) + ' NO')
            else:
                if obj in graph[subj][0]:
                    output.append(','.join(line_list) + ' YES')
                else:
                    output.append(','.join(line_list) + ' NO')
            end_time = time.perf_counter()
            if args.time:
                print(f'{line.strip()}: {end_time - start_time}s')
        else:
            start_time = time.perf_counter()
            _, obj1, obj2 = line_list
            queue = collections.deque()
            queue.append(obj1)
            vis = {obj1}
            found = False
            while queue:  # BFS the directed graph to find if there is a path from obj1 to obj2
                curr = queue.popleft()
                if curr == obj2:
                    output.append(','.join(line_list) + ' YES')
                    found = True
                    break
                for nei in graph[curr][0]:
                    if nei not in vis:
                        vis.add(nei)
                        queue.append(nei)
            if not found:
                output.append(','.join(line_list) + ' NO')
            end_time = time.perf_counter()
            if args.time:
                print(f'{line.strip()}: {end_time - start_time}s')

with open(output_file, 'w') as f:
    f.write('\n'.join(output) + '\n')