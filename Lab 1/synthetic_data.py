import numpy as np
import pprint

from numpy.random.mtrand import randint

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
    def create_kleinberg_graph(n, m, clustering_exponent=2):
        # Start from the grid graph
        graph = SyntheticGraphGenerator.create_grid_graph(n, m)

        all_nodes = []
        for i in range(n):
            for j in range(m):
                all_nodes.append([i, j, f'{i}_{j}'])

        for it, (src_i, src_j, src) in enumerate(all_nodes):
            for (dest_i, dest_j, dest) in all_nodes[it + 1:]:
                # Compute edge probability for `small world` effect
                dist = np.abs(src_i - dest_i) + 1 + np.abs(src_j - dest_j) + 1
                prob = 1 / dist ** clustering_exponent

                # Add edge with probability
                rnd = np.random.rand()
                if rnd <= prob:
                    graph.add_edge(src, dest)

        return graph

    @staticmethod
    def create_tree_graph(num_nodes):
        graph = Graph(edge_type=EdgeType.UNDIRECTED)
        graph.add_node(0)  # Root node
        for i in range(1, num_nodes):
            graph.add_node(i)
            # Chooose parent at random amongst the i-1 nodes already introduced
            parent = np.random.randint(0, i)
            graph.add_edge(i, parent)

        return graph

    @staticmethod
    def create_split_graph(clique_size, stable_set_size, prob=0.3):
        graph = Graph(edge_type=EdgeType.UNDIRECTED)

        # Create clique
        clique_nodes = []
        for i in range(clique_size):
            node = f'clq_#{i}'
            graph.add_node(node)
            clique_nodes.append(node)

            # Add edges to all previous nodes
            for neigh in clique_nodes[:-1]:
                graph.add_edge(node, neigh)

        # Create stable set
        stable_set_nodes = []
        for i in range(stable_set_size):
            node = f'ss_#{i}'
            graph.add_node(node)
            stable_set_nodes.append(node)

        # Add edges between clique and stable set
        for clq_node in clique_nodes:
            for ss_node in stable_set_nodes:
                rnd = np.random.rand()
                if rnd <= prob:
                    graph.add_edge(clq_node, ss_node)

        return graph


def main():
    pp = pprint.PrettyPrinter(indent=4)

    print('Random graph:')
    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=10, edge_prob=0.5)
    pp.pprint(random_graph.adjacency_list)

    print('Grid graph:')
    grid_graph = SyntheticGraphGenerator.create_grid_graph(n=5, m=7)
    pp.pprint(grid_graph.adjacency_list)

    print('Kleinberg graph:')
    kleinberg_graph = SyntheticGraphGenerator.create_kleinberg_graph(n=5, m=7)
    pp.pprint(kleinberg_graph.adjacency_list)

    print('Tree graph:')
    tree_graph = SyntheticGraphGenerator.create_tree_graph(num_nodes=10)
    pp.pprint(tree_graph.adjacency_list)

    print('Split graph:')
    split_graph = SyntheticGraphGenerator.create_split_graph(clique_size=5, stable_set_size=5)
    pp.pprint(split_graph.adjacency_list)


if __name__ == '__main__':
    main()
