import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import pprint

from matplotlib.ticker import MaxNLocator, AutoLocator

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


def clustering_coefficients(graph, name=''):
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

    # Make bar plot for coefficient count
    coeffs = list(coeff.values())
    coeffs = list(map(lambda c: round(c, 2), coeffs))
    coeffs = pd.DataFrame(coeffs, columns=['clustering_coefficient'])
    coeffs = coeffs['clustering_coefficient'].value_counts().sort_index()
    coeffs.plot(kind='bar', rot=45, width=1.3)

    plt.title(f'Clustering coefficients distribution\n{name}')
    # plt.gca().xaxis.set_major_locator(MaxNLocator(min(25, len(coeffs))))
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.xlabel('Clustering coefficient')
    plt.ylabel('Count')

    plt.tight_layout()
    plt.show()

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

    average_distance = np.array(distances).mean()
    label = ''

    if average_distance < np.log(np.log(len(graph.nodes))):
        label = 'ultra small world'
    elif average_distance < np.log(len(graph.nodes)):
        label = 'small world'

    return average_distance, label


def main():
    pp = pprint.PrettyPrinter(indent=4)

    graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=500, edge_prob=0.01)
    # pp.pprint(graph.adjacency_list)
    # print(f'Random graph: num_traingles = {count_triangles(graph)}')

    coeff = clustering_coefficients(graph)
    print('Random graph: clustering coefficients')
    pp.pprint(coeff)

    avg_dist = compute_average_distance(graph)
    print(f'Random graph: average distance = {avg_dist}')


if __name__ == '__main__':
    main()
