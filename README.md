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

├───study.pdf  
├───data  
│   ├───cut_visualizations       
│   ├───graphs  
│   ├───partition_visualizations  
│   ├───plots  
│   └───results_csv  
└───src  
    ├───data_analysis  
    │       draw_graph_and_min_cut.py  
    │       results_analysis.R  
    │       time_analysis.R  
    │       
    ├───graph_generation  
    │       create_graphs.py  
    │       graph_generator.py  
    │       
    └───solve  
        ├───algorithm_tracker.py  
        ├───solve_exhaustive_partition.py  
        ├───solve_exhaustive_remove_edges.py  
        ├───solve_greedy.py  
        ├───solve_greedy_partitions.py  
        └───visited_monitor.py  