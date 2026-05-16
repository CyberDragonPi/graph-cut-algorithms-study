# Graph Partitioning & Minimum Cut Algorithms

This project implements and compares different algorithms for the **Minimum Cut problem** in undirected, unweighted graphs. 
It was developed as part of the Advanced Algorithms course at the University of Aveiro.

It includes both **exact (exhaustive)** and **heuristic (greedy)** approaches, along with experimental evaluation of performance and scalability.

---

## Algorithms

### Exact Methods
- Edge subset enumeration (brute force over edges)
- Vertex partition enumeration (brute force over node partitions)

### Greedy Methods
- Greedy edge removal
- Greedy partitioning (inspired by Kernighan–Lin style heuristics)

---

## Project Structure

study.pdf                # Theoretical report (8 pages)  
data/  
├── graphs/              # Generated graph instances  
├── cut_visualizations/  # Min-cut visualizations  
├── partition_visualizations/  
├── plots/               # Experimental plots  
└── results_csv/         # Experimental results  
  
src/  
├── graph_generation/    # Graph generators  
├── solve/               # Algorithm implementations  
└── data_analysis/       # Plotting and analysis scripts


## Tech Stack

- Python (NetworkX) – algorithm implementation and graph processing  
- R – experimental analysis and visualization  
- GraphML – graph data format  
- Matplotlib – performance plots and result visualization  
