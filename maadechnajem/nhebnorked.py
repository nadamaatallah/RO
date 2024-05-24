import osmnx as ox
import networkx as nx
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def extract_graph(place_name):
    graph = ox.graph_from_place(place_name, network_type="all")
    return graph

def calculate_edge_speeds(graph):
    ox.speed.add_edge_speeds(graph)
    return graph

def create_directed_graph(graph):
    G = nx.DiGraph()
    for u, v, data in graph.edges(data=True):
        attrs = data.copy()
        if attrs['oneway'] == 'True':
            G.add_edge(u, v, **attrs)
        else:
            G.add_edge(u, v, **attrs)
            G.add_edge(v, u, **attrs)
    return G

def calculate_edge_travel_times(graph):
    for u, v, data in graph.edges(data=True):
        length_km = data['length']
        speed_kph = data['speed_kph']
        travel_time = length_km / speed_kph if speed_kph != 0 else float('inf')
        graph[u][v]['weight'] = travel_time
    return graph

def dijkstra_shortest_path(graph, source, target):
    shortest_path, shortest_path_length = nx.single_source_dijkstra(graph, source, target=target, weight='weight')
    return shortest_path, shortest_path_length

def bellman_ford_shortest_path(graph, source, target):
    shortest_path = nx.bellman_ford_path(graph, source, target=target, weight='weight')
    shortest_path_length = nx.bellman_ford_path_length(graph, source, target=target, weight='weight')
    return shortest_path, shortest_path_length

@app.route('/')
def index():
    return render_template('nhebnorked.html')

@app.route('/optimize_route', methods=['POST'])
def optimize_route():
    data = request.json
    source = (data['source']['lat'], data['source']['lng'])
    target = (data['target']['lat'], data['target']['lng'])
    algorithm = data['algorithm']
    
    graph = extract_graph("Ariana, Tunis")
    graph = calculate_edge_speeds(graph)
    graph = create_directed_graph(graph)
    graph = calculate_edge_travel_times(graph)

    source_node = ox.distance.nearest_nodes(graph, source[1], source[0])
    target_node = ox.distance.nearest_nodes(graph, target[1], target[0])

    if algorithm == 'dijkstra':
        shortest_path, shortest_path_length = dijkstra_shortest_path(graph, source_node, target_node)
    elif algorithm == 'bellman-ford':
        shortest_path, shortest_path_length = bellman_ford_shortest_path(graph, source_node, target_node)
    else:
        return jsonify({"error": "Invalid algorithm"})

    if shortest_path:
        return jsonify({"shortest_path": shortest_path, "shortest_path_length": shortest_path_length})
    else:
        return jsonify({"error": "No path found"})

if __name__ == "__main__":
    app.run(debug=True)
