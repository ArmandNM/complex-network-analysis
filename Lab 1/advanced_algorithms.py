import pprint

from synthetic_data import SyntheticGraphGenerator
from basic_algorithms import compute_degree_sequence


def count_triangles(graph):
    num_triangles = 0

    # Run a depth 2 DFS from each node
    for start_node in graph.nodes:
        for neigh1 in graph.get_neighbours(start_node):
            for neigh2 in graph.get_neighbours(neigh1):
                # Don't return to parent
                if neigh2 == start_node:
                    continue
                for neigh3 in graph.get_neighbours(neigh2):
                    # If returned to start_node, we found a triangle
                    if neigh3 == start_node:
                        num_triangles += 1

    # Remove counting redundancy
    return num_triangles // 6


def clustering_coefficients(graph):
    coeff = {}

    # Compute the degree sequence
    degree = compute_degree_sequence(graph)

    # Run a depth 2 DFS from each node
    for start_node in graph.nodes:
        num_triangles = 0
        for neigh1 in graph.get_neighbours(start_node):
            for neigh2 in graph.get_neighbours(neigh1):
                # Don't return to parent
                if neigh2 == start_node:
                    continue
                for neigh3 in graph.get_neighbours(neigh2):
                    # If returned to start_node, we found a triangle
                    if neigh3 == start_node:
                        num_triangles += 1

        # Each triangle was counted twice
        num_triangles = num_triangles // 2

        # Compute the theoretical maximum possible number of triangles
        max_triangles = degree[start_node] * (degree[start_node] - 1) / 2

        if max_triangles > 0:
            coeff[start_node] = num_triangles / max_triangles
        else:
            coeff[start_node] = 0

    return coeff


def main():
    pp = pprint.PrettyPrinter(indent=4)

    graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=5, edge_prob=0.5)
    pp.pprint(graph.adjacency_list)
    print(f'Random graph: num_traingles = {count_triangles(graph)}')

    coeff = clustering_coefficients(graph)
    print('Random graph: clustering coefficients')
    pp.pprint(coeff)


if __name__ == '__main__':
    main()
