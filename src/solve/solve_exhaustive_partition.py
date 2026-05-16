import networkx
import glob
import os
import time
import itertools
import pandas

from pathlib import Path
from algorithm_tracker import AlgorithmTracker


def generate_node_partitions(nodes: list, V: int):
    partitions = []

    nodes = [int(u) for u in nodes]

    for r in range(1, V //2 + 1):
        for subset in itertools.combinations(nodes, r):
            S = set(subset)
            T = set(nodes) - S
            partitions.append((S, T))

    return partitions


def solve_by_partition(G: networkx.Graph, algorithm_tracker: AlgorithmTracker):
    nodes = G.nodes()
    edges = G.edges()
    V = len(nodes)
    E = len(edges)
    partitions = []

    A = [[0 for column in range(V)] for row in range(V)]
    for (a, b) in edges:
        A[int(a)][int(b)] = 1
        A[int(b)][int(a)] = 1

    partitions = generate_node_partitions(nodes, V)
    
    minimum_number_of_bridges = E
    best_S = set()
    best_T = set()

    algorithm_tracker.start_time = time.time()

    for (S, T) in partitions:
        algorithm_tracker.solutions_tested += 1
        current_number_of_bridges = 0

        for u in S:
            for v in T:
                current_number_of_bridges += A[u][v]
                algorithm_tracker.basic_operations += 1

        if current_number_of_bridges < minimum_number_of_bridges:
            minimum_number_of_bridges = current_number_of_bridges
            best_S = S
            best_T = T

        if current_number_of_bridges == 1:
            break

    algorithm_tracker.end_time = time.time()
    return A, minimum_number_of_bridges, best_S, best_T, algorithm_tracker


def get_bridges(A: list[list[int]], S: set[int], T: set[int]):
    bridges = set()

    for u in S:
        for v in T:
            if A[u][v] == 1:
                bridges.add(tuple(sorted([u, v])))

    return bridges



RESULTS_DIR = "data/results_csv/"
GRAPHS_DIR = "data/graphs"

if __name__ == "__main__":
    graphml_files = glob.glob(os.path.join(GRAPHS_DIR, "*.graphml"))
    results_partition = []

    for file_path in graphml_files:
        graph_name = os.path.splitext(os.path.basename(file_path))[0]
        G = networkx.read_graphml(file_path)
        print(f"Loaded graph with V={G.number_of_nodes()} and E={G.number_of_edges()}")
        
        algorithm_tracker = AlgorithmTracker() 
        A, min_number_of_bridges, S, T, algorithm_tracker = solve_by_partition(G, algorithm_tracker)
        edges_to_remove = get_bridges(A, S, T)

        results_partition.append({
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "min_cut": min_number_of_bridges,
            "edges_to_remove": edges_to_remove,
            "solutions_tested": algorithm_tracker.solutions_tested,
            "basic_operations": algorithm_tracker.basic_operations,
            "time_elapsed": algorithm_tracker.end_time - algorithm_tracker.start_time
        })

        print(f"-----------------------------------")


    results = sorted(results_partition, key=lambda x: (x["nodes"], x["edges"]))
    dataframe_partition = pandas.DataFrame(results)
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    dataframe_partition.to_csv("data/results_csv/min_cut_partition_results.csv", index=False)