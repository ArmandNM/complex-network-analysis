import numpy as np

from graph import Graph, EdgeType


class SyntheticGraphGenerator:
    def __init__(self):
        pass

    @staticmethod
    def create_random_edge_graph(num_nodes, edge_prob):
        graph = Graph(edge_type=EdgeType.UNDIRECTED)
        for i in range(num_nodes):
            # Update nodes set
            graph.add_node(i)

            # Add edge i, j with probabilitty `edge_prob`
            for j in range(i + 1, num_nodes):
                rnd = np.random.rand()
                if rnd <= edge_prob:
                    graph.add_node(j)
                    graph.add_edge(i, j)

        return graph


def main():
    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=10, edge_prob=0.5)
    print(random_graph.adjacency_list)


if __name__ == '__main__':
    main()
