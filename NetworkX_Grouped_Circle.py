import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

# Load your JSON data
with open('pokemon-showdown.json') as f:
    data = json.load(f)

# Helper function to check if a file is in the test folder
def is_in_test_folder(file_path):
    return file_path.startswith("test/")

# Group files by directory
directory_files = defaultdict(list)
file_to_directory = {}

for file, details in data.items():
    if not is_in_test_folder(file):
        directory = file.split('/')[0]  # Assuming directory is the first part of the file path
        directory_files[directory].append(file)
        file_to_directory[file] = directory

# Create a new directed graph for directories
G = nx.DiGraph()

# Add nodes with size based on number of files
for directory, files in directory_files.items():
    G.add_node(directory, size=len(files))

# Add edges with weight based on number of dependencies
edge_weights = defaultdict(int)

for file, details in data.items():
    if not is_in_test_folder(file) and details['adjacentTo']:
        source_directory = file_to_directory.get(file)
        for adjacent in details['adjacentTo']:
            if not is_in_test_folder(adjacent):
                target_directory = file_to_directory.get(adjacent)
                if source_directory and target_directory and source_directory != target_directory:
                    edge_weights[(source_directory, target_directory)] += 1

for (source, target), weight in edge_weights.items():
    G.add_edge(source, target, weight=weight)

# Draw the graph with node sizes and edge widths using a circular layout
pos = nx.circular_layout(G)
node_sizes = [G.nodes[node]['size'] * 100 for node in G.nodes]  # Scale node sizes
edge_widths = [G.edges[edge]['weight'] for edge in G.edges]  # Use edge weights for widths

plt.figure(figsize=(12, 8))

# Draw nodes and labels
nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue")
nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

# Draw edges with arrows
edges = nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=50, edge_color='gray', width=edge_widths)

plt.title("Pokemon Showdown Graph Grouped by Directory")
plt.show()
