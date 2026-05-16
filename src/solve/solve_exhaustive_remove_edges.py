import networkx
import glob
import os
import numpy
import itertools
import pandas
import time

from pathlib import Path
from algorithm_tracker import AlgorithmTracker
from visited_monitor import VisitedMonitor


def generate_egde_subsets(edges: list, algorithm_tracker: AlgorithmTracker):
    nodes_degrees = dict()

    for (u, v) in edges:
        if u not in nodes_degrees:
            nodes_degrees[u] = 0
        if v not in nodes_degrees:
            nodes_degrees[v] = 0

        nodes_degrees[u] += 1
        nodes_degrees[v] += 1

    lowest_degree = -1
    for node in nodes_degrees:
        if lowest_degree == -1 or lowest_degree > nodes_degrees[node]:
            lowest_degree = nodes_degrees[node] 

    edge_subsets = []
    for r in range(1, lowest_degree + 1):
        for subset in itertools.combinations(edges, r):
            edge_subsets.append(set(subset))

            if time.time() - algorithm_tracker.start_time > 60:
                return set(), -1
    
    return edge_subsets, 1


def floodfill(current_node: int, graph: networkx.Graph, visited_monitor: VisitedMonitor, algorithm_tracker: AlgorithmTracker):
    visited_monitor.visited[current_node] = 1
    algorithm_tracker.basic_operations += 1

    for v in graph.neighbors(current_node):
        if visited_monitor.visited[v] == 0:
            floodfill(v, graph, visited_monitor, algorithm_tracker)


def check_connected(graph: networkx.Graph, starting_node: int, V: int, algorithm_tracker: AlgorithmTracker) -> bool:
    visited_monitor = VisitedMonitor(V)
    algorithm_tracker.solutions_tested += 1
    floodfill(starting_node, graph, visited_monitor, algorithm_tracker)
    return (sum(visited_monitor.visited) == visited_monitor.V)


def solve_by_removing_edges(G: networkx.Graph, algorithm_tracker: AlgorithmTracker):
    algorithm_tracker.start_time = time.time()
    nodes = G.nodes()
    edges = G.edges()

    nodes = [int(u) for u in nodes]
    edges = set([(int(u), int(v)) for (u, v) in edges])
    edge_subsets, success = generate_egde_subsets(edges, algorithm_tracker)

    if success == -1:
        return -1, set(), algorithm_tracker

    
    min_cut = set()
    min_number = len(edges)
    algorithm_tracker.start_time = time.time()

    for edges_to_remove in edge_subsets:
        current_edges = edges - edges_to_remove
        current_G = networkx.Graph()
        current_G.add_nodes_from(nodes)
        current_G.add_edges_from(current_edges)
        
        if not check_connected(current_G, 0, len(nodes), algorithm_tracker) and len(edges_to_remove) < min_number:
            min_number = len(edges_to_remove)
            min_cut = edges_to_remove

        if min_number == 1:
            break

        if time.time() - algorithm_tracker.start_time > 120:
            return -1, set(), algorithm_tracker
        
    
    algorithm_tracker.end_time = time.time()
    return min_number, min_cut, algorithm_tracker


RESULTS_DIR = "data/results_csv/"
GRAPHS_DIR = "data/graphs/"

if __name__ == "__main__":
    graphml_files = glob.glob(os.path.join(GRAPHS_DIR, "*.graphml"))

    graphs_info = []
    for file_path in graphml_files:
        G = networkx.read_graphml(file_path)
        graphs_info.append((file_path, G.number_of_nodes(), G.number_of_edges()))

    graphs_info.sort(key=lambda x: (x[1], x[2]))
    results_remove_edges = []

    for (file_path, _, _) in graphs_info:
        graph_name = os.path.splitext(os.path.basename(file_path))[0]
        G = networkx.read_graphml(file_path)
        print(f"Loaded graph with V={G.number_of_nodes()} and E={G.number_of_edges()}")

        algorithm_tracker = AlgorithmTracker() 
        min_number_of_bridges, edges_to_remove, algorithm_tracker = solve_by_removing_edges(G, algorithm_tracker)

        results_remove_edges.append({
            "graph": graph_name,
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "min_cut": min_number_of_bridges,
            "edges_to_remove": edges_to_remove,
            "solutions_tested": algorithm_tracker.solutions_tested,
            "basic_operations": algorithm_tracker.basic_operations,
            "time_elapsed": algorithm_tracker.end_time - algorithm_tracker.start_time
        })

        print(f"-----------------------------------")

    results = sorted(results_remove_edges, key=lambda x: (x["nodes"], x["edges"]))
    dataframe_partition = pandas.DataFrame(results)
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    dataframe_partition.to_csv("data/results_csv/min_cut_removing_edges_results.csv", index=False)