import numpy as np
import random
import pprint

from synthetic_data import SyntheticGraphGenerator
from basic_algorithms import compute_degree_sequence, breadth_first_search


def count_triangles(graph):
    num_triangles = {}

    # Run a depth 2 DFS from each node
    for start_node in graph.nodes:
        num_triangles[start_node] = 0
        for neigh1 in graph.get_neighbours(start_node):
            for neigh2 in graph.get_neighbours(neigh1):
                # Don't return to parent
                if neigh2 == start_node:
                    continue
                for neigh3 in graph.get_neighbours(neigh2):
                    # If returned to start_node, we found a triangle
                    if neigh3 == start_node:
                        num_triangles[start_node] += 1

        # Each triangle was counted twice for start_node
        num_triangles[start_node] = num_triangles[start_node] // 2

    total = 0
    for node in num_triangles.keys():
        total += num_triangles[node]

    # Each triangle was counted once for every of its vertices
    return total // 3, num_triangles


def clustering_coefficients(graph):
    coeff = {}

    # Compute the degree sequence
    degree = compute_degree_sequence(graph)

    # Get number of triangles foro each vertex
    _, num_triangles = count_triangles(graph)

    for node in graph.nodes:
        # Compute the theoretical maximum possible number of triangles
        max_triangles = degree[node] * (degree[node] - 1) / 2

        if max_triangles > 0:
            coeff[node] = num_triangles[node] / max_triangles
        else:
            coeff[node] = 0

    return coeff


def compute_average_distance(graph, num_samples=1000):
    distances = []

    for _ in range(num_samples):
        src = random.choice(list(graph.nodes))
        dest = random.choice(list(graph.nodes))

        if src == dest:
            continue

        _, out = breadth_first_search(graph, src)

        # Check if src and dest are connected
        res = list(filter(lambda o: o[0] == dest, out))
        if len(res) > 0:
            distances.append(res[0][1])

    return np.array(distances).mean()


def main():
    pp = pprint.PrettyPrinter(indent=4)

    graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=5000, edge_prob=0.01)
    # pp.pprint(graph.adjacency_list)
    print(f'Random graph: num_traingles = {count_triangles(graph)}')

    coeff = clustering_coefficients(graph)
    print('Random graph: clustering coefficients')
    pp.pprint(coeff)

    avg_dist = compute_average_distance(graph)
    print(f'Random graph: average distance = {avg_dist}')


if __name__ == '__main__':
    main()
