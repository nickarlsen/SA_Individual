import json
import graphviz
import os

def create_dependency_graph(json_data):
    graph = graphviz.Digraph(format='png')

    # Dictionary to hold subgraphs for each directory cluster
    clusters = {}

    # Create nodes and clusters
    for file, attributes in json_data.items():
        directory = os.path.dirname(file)
        
        # Create a new cluster if it doesn't exist
        if directory not in clusters:
            clusters[directory] = graphviz.Digraph(name=f'cluster_{directory}')
            clusters[directory].attr(label=directory, style='filled', color='lightgrey')

        # Add node to the respective cluster
        clusters[directory].node(file)

    # Add all clusters to the main graph
    for cluster in clusters.values():
        graph.subgraph(cluster)

    # Add edges to the graph
    for file, attributes in json_data.items():
        for adjacent in attributes.get("adjacentTo", []):
            graph.edge(file, adjacent)

    return graph

# Load JSON data from a file
with open('pokemon-showdown.json', 'r') as f:
    data = json.load(f)

# Create the dependency graph
graph = create_dependency_graph(data)

# Save and render the graph
graph.render('clustered_dependency_graph', view=True)
