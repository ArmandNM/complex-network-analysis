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

    @staticmethod
    def create_grid_graph(n, m):
        graph = Graph(edge_type=EdgeType.UNDIRECTED)

        # Define grid direction offsets
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        for i in range(n):
            for j in range(m):
                src = f'{i}_{j}'  # Construct src node id
                graph.add_node(src)

                # Connect to all 4 neighbours
                for k in range(4):
                    # Compute grid coordinates
                    neigh_i = i + dy[k]
                    neigh_j = j + dx[k]

                    # Make sure we are still in the grid
                    if neigh_i < 0 or neigh_i >= n:
                        continue
                    if neigh_j < 0 or neigh_j >= m:
                        continue

                    dest = f'{neigh_i}_{neigh_j}'  # Construct dest node id
                    graph.add_node(dest)
                    graph.add_oriented_edge(src, dest)

        return graph

    @staticmethod
    def create_kleinberg_graph():
        pass

    @staticmethod
    def create_tree_graph():
        pass

    @staticmethod
    def create_split_graph():
        pass


def main():
    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=10, edge_prob=0.5)
    grid_graph = SyntheticGraphGenerator.create_grid_graph(n=5, m=7)
    print(random_graph.adjacency_list)
    print(grid_graph.adjacency_list)


if __name__ == '__main__':
    main()
