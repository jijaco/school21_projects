import matplotlib.pyplot as plt
import networkx as nx
import json
from pyvis.network import Network


def multiply_vector(nodes: list, n: int):
    for i in range(len(nodes)):
        nodes[i] *= n


G = nx.DiGraph(directed=True)
with open('../rel.yml', 'r') as f:
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
size_of_nodes = [x[i] for i in x]

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
    net.nodes[k]['size'] = size_of_nodes[k] * 10
    k += 1
multiply_vector(size_of_nodes, 300)
nx.draw(G, pos, with_labels=True, arrows=True,
        node_size=size_of_nodes, **options)
net.save_graph('wiki_graph.html')
plt.savefig("Graph.png", format="PNG", dpi=1000)
