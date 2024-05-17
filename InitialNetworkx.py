import json
import networkx as nx
import matplotlib.pyplot as plt

# Load your JSON data
with open('pokemon-showdown.json') as f:
    data = json.load(f)

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges to the graph
for file, details in data.items():
    if details['adjacentTo']:
        G.add_node(file)
        for adjacent in details['adjacentTo']:
            G.add_edge(file, adjacent)

# Remove nodes with no adjacentTo
nodes_to_remove = [node for node in G.nodes if G.in_degree(node) == 0 and G.out_degree(node) == 0]
G.remove_nodes_from(nodes_to_remove)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=7000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
plt.show()
