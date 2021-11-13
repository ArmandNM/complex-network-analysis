import numpy as np
import matplotlib.pyplot as plt
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(11000)
print(sys.getrecursionlimit())

from matplotlib.ticker import MaxNLocator

from synthetic_data import SyntheticGraphGenerator
from basic_algorithms import get_connected_components, compute_diameter, compute_girth


def distribution_of_connected_components(graph):
    cc = get_connected_components(graph)
    cc_sizes = list(map(lambda comp: len(comp), cc))
    print(cc_sizes)

    # fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(7.5, 5.5))
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    # ax.locator_params(axis='both', integer=True)
    # ax.ticklabel_format(useOffset=False)
    # ax.set_ylim(xmin=0)
    # ax.set_xlim(xmin=0)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(cc_sizes, cc_sizes)
    # ax.set_aspect('auto')
    # ax.set_xbound(lower=-100, upper=1100)
    # ax.ticklabel_format(style='plain', useOffset=False, axis='both')
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.ticklabel_format(style='plain')

    plt.savefig('tests.png')

    # print(cc_sizes)
    # bins = np.linspace(start=0, stop=max(cc_sizes)+1000, num=10)
    # ax.set_xticks(bins)

    # plt.hist(x=cc_sizes, bins=100)
    # plt.autoscale()

    # bins = list(range(0, int(max(cc_sizes) / 100)))

    # bins = np.arange(0, max(cc_sizes) + 1.5) + 0.5
    # plt.hist(x=cc_sizes, color='blue', edgecolor='black', bins=bins)

    # plt.xticks(range(10))
    # plt.xticks(bins - 0.5)

    # plt.title('Distribution of connected components')
    # plt.xlabel('Size')
    # plt.ylabel('# Components')
    plt.show()


def diameter_classification(graph, num_repeats=20):
    # Use 2 DFS method multiple times to estimate graph diameter
    diameters = []
    for _ in range(num_repeats):
        diameter, _, _ = compute_diameter(graph, start_node='random')
        diameters.append(diameter)

    diameter = np.array(diameters).mean()

    ratio = diameter / np.log(len(graph.nodes))

    # Classify based on diameter / log(n) ratio
    if ratio <= 1:
        return 0
    elif 1 < ratio <= 10:
        return 1
    elif ratio > 10:
        return 2


def girth_classification(graph):
    girth = compute_girth(graph)

    if girth <= 4:
        return 0
    elif girth > 4:
        return 1


def main():
    graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=100, edge_prob=0.01)
    print(f'Random graph: diameter type #{diameter_classification(graph)}.')
    print(f'Random graph: girth type #{girth_classification(graph)}.')

    graph = SyntheticGraphGenerator.create_grid_graph(n=10, m=21)
    print(f'Grid graph: diameter type #{diameter_classification(graph)}.')
    print(f'Grid graph: girth type #{girth_classification(graph)}.')


if __name__ == '__main__':
    main()
