import itertools

from graph_generator import Generator


if __name__ == "__main__":
    Vs: list[int] = [x for x in range(3, 25)]
    ks: list[float] = [0.125, 0.25, 0.5, 0.75, 1]
    N = 3

    for V, k in itertools.product(Vs, ks):
        print(f"Generating graph with V={V}, k={k}")

        generator = Generator(V, k, student_number=130288, distance_threshold=10, max_neighbours=V - 1, max_weight=0)

        if V >= 8 and k < 1:
            iterations = 5
        else:
            iterations = 1
        
        for i in range(iterations):
            graph = generator.generate_graph()
            while not generator.check_connected(0, graph):
                print("Generation failed. Generating again.")
                graph = generator.generate_graph()

            generator.save_graph(graph, i)

    