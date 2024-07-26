from collections import deque
import argparse
import json
import os
import pathlib

if 'WIKI_FILE' not in os.environ or not pathlib.Path(os.environ['WIKI_FILE']).exists():
    print("database not found")
    exit(1)

location_of_graph = os.environ.get('WIKI_FILE')

with open(location_of_graph, "r") as fp:
    graph = json.load(fp)

parser = argparse.ArgumentParser(
    prog='shortest_path',
    description='What the program does',
    epilog='Text at the bottom of help')

parser.add_argument('-v', '--view', action=argparse.BooleanOptionalAction)
parser.add_argument('--from', dest='from_')
parser.add_argument('--to')
parser.add_argument('--non-directed', dest='direction', action=argparse.BooleanOptionalAction)

args = parser.parse_args()


def in_graph(graph, key):
    for k, v in graph.items():
        if key in graph[k] or key in graph:
            return True
    return False


if args.from_ is None or args.to is None:
    print("No necessary arguments provided")
    exit(1)
elif not in_graph(graph, args.from_) or not in_graph(graph, args.to):
    print("No vertices found in graph with this title")
    exit(1)

if args.direction is not None:
    for k, v in graph.items():
        for vertice in v:
            if vertice not in graph:
                graph[vertice] = []
            graph[vertice].append(k)


def bfs_search(graph, S, par, dist):
    q = deque()
    dist[S] = 0
    q.append(S)

    while q:
        node = q.popleft()

        for neighbor in graph[node]:
            if neighbor in dist and dist[neighbor] == float('inf'):
                par[neighbor] = node
                dist[neighbor] = dist[node] + 1
                q.append(neighbor)


def print_shortest_distance(graph, S, D, V):
    par = dict(graph)

    dist = dict(graph)

    for k, v in par.items():
        par[k] = -1

    for k, v in dist.items():
        dist[k] = float('inf')

    bfs_search(graph, S, par, dist)

    if dist[D] == float('inf'):
        print("path not found")
        return

    path = []
    current_node = D
    path.append(D)
    while par[current_node] != -1:
        path.append(par[current_node])
        current_node = par[current_node]

    if args.view is not None:
        for i in range(len(path) - 1, -1, -1):
            if i != len(path) - 1:
                print(" -> ", end='')
            print(path[i], end="")
        print()
    print(len(path))


print_shortest_distance(graph, args.from_, args.to, len(graph))
