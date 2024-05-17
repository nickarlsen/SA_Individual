import json
import graphviz

# Function to create a graph from JSON data
def create_dependency_graph(json_data):
    graph = graphviz.Digraph(format='png')

    # Add nodes and edges to the graph
    for file, attributes in json_data.items():
        graph.node(file)
        for adjacent in attributes.get("adjacentTo", []):
            graph.edge(file, adjacent)
    
    return graph

# Load JSON data from a file
with open('pokemon-showdown.json', 'r') as f:
    data = json.load(f)

# Create the dependency graph
graph = create_dependency_graph(data)

# Save and render the graph
graph.render('dependency_graph', view=True)
