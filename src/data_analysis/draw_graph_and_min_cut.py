import ast
import glob
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

GRAPHS_DIR = "data/graphs/"

if __name__ == "__main__":
    graphml_files = glob.glob(os.path.join(GRAPHS_DIR, "*.graphml"))

    data = pd.read_csv("data/results_csv/min_cut_greedy_partition_results.csv")

    for file_path in graphml_files:
        graph_name = os.path.splitext(os.path.basename(file_path))[0]

        row = data[data["graph"] == graph_name]
        if row.empty:
            print(f"No result found for {graph_name}, skipping...")
            continue

        row = row.iloc[0]

        G = nx.read_graphml(file_path)
        print(f"Loaded {graph_name} with V={G.number_of_nodes()} and E={G.number_of_edges()}")

        cut_edges = ast.literal_eval(row["edges_to_remove"])

        cut_edges = []
        for u, v in ast.literal_eval(row["edges_to_remove"]):
            u, v = str(u), str(v)
            if G.has_edge(u, v):
                cut_edges.append((u, v))
            elif G.has_edge(v, u):  
                cut_edges.append((v, u))

        pos = {
                node: tuple(map(float, data["pos"].split(",")))
                for node, data in G.nodes(data=True)
                    if "pos" in data}

        if G.number_of_nodes() > 15:
            fig_size = 8
        else:
            fig_size = 4
        plt.figure(figsize=(fig_size, fig_size))

        nx.draw(G, pos, with_labels=True, node_size=400, edge_color="gray")

        if cut_edges:
            nx.draw_networkx_edges(G, pos, edgelist=cut_edges, edge_color="red", width=3)
        else:
            print(f"No valid cut edges found for {graph_name}")

        plt.tight_layout()

        out_path = f"cut_visualizations/{graph_name}"
        os.makedirs("cut_visualizations", exist_ok=True)
        plt.savefig(f"{out_path}.pdf", format="pdf", bbox_inches='tight')
        print(f"Saved visualization to {out_path}")
        plt.close()
