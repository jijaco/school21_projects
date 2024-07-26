import matplotlib.pyplot as plt
import networkx as nx
import json
from pyvis.network import Network
import os
import pathlib

if 'WIKI_FILE' not in os.environ or not pathlib.Path(os.environ['WIKI_FILE']).exists():
    print("database not found")
    exit(1)


def multiply_vector(nodes: list, n: int):
    for i in range(len(nodes)):
        nodes[i] *= n


G = nx.DiGraph(directed=True)
with open(os.environ['WIKI_FILE'], 'r') as f:
    data = json.load(f)

s: set = set()
for i in data:
    s.add(i)
    if isinstance(data[i], list) or isinstance(data[i], tuple):
        for j in data[i]:
            s.add(j)
    else:
        s.add(data[i])

x: dict = {}
for i in [*s]:
    x[i] = 1
for i in data:
    if isinstance(data[i], list) or isinstance(data[i], tuple):
        for j in data[i]:
            x[j] += 1
    else:
        x[data[i]] += 1

G.add_nodes_from([*s])
size_of_nodes = [x[i] ** 2 for i in x]

for i in [*data]:
    if isinstance(data[i], list) or isinstance(data[i], tuple):
        for j in data[i]:
            G.add_edge(i, j)
    else:
        G.add_edge(i, data[i])

options = {'arrowstyle': '-|>'}
order = G.nodes
pos = nx.circular_layout(G)
net = Network(directed=True)
net.repulsion()
net.add_nodes(G.nodes)
net.add_edges(G.edges)
k = 0
for i in G.nodes:
    net.nodes[k]['size'] = size_of_nodes[k]
    k += 1
multiply_vector(size_of_nodes, 100)
nx.draw(G, pos, with_labels=True, arrows=True,
        node_size=size_of_nodes, **options)
net.save_graph('wiki_graph.html')
plt.savefig("Graph.png", format="PNG", dpi=1000)
