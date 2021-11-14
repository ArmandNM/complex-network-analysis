import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import sys

from matplotlib.ticker import MaxNLocator

from main import prepare_data
from synthetic_data import SyntheticGraphGenerator
from basic_algorithms import get_connected_components, compute_diameter, compute_girth

print(sys.getrecursionlimit())
sys.setrecursionlimit(11000)
print(sys.getrecursionlimit())


def test_pandas():
    df = pd.read_csv('./test_data/archive/condensed_day_report.csv')
    df['day_of_week'].value_counts()[:20].plot(kind='bar')
    plt.show()


def distribution_of_connected_components(graph, name='fb'):
    cc = get_connected_components(graph)

    # Count connected components sizes
    cc_sizes = list(map(lambda comp: len(comp), cc))

    # Convert to dataframe for easier plotting
    cc_sizes = pd.DataFrame(cc_sizes, columns=['size'])

    # Aggregate by size
    cc_sizes = cc_sizes['size'].value_counts().sort_index()

    # Determine if graph has a `big component`
    sizes = cc_sizes.iloc[-2:].index.tolist()
    counts = cc_sizes.iloc[-2:].tolist()

    big_component = False
    if sizes[-1] > len(graph.nodes) / 100 and counts[-1] == 1:  # a single big component
        big_component = True

    if len(sizes) == 2 and sizes[-2] > np.log(len(graph.nodes)) / 2:
        big_component = False

    # Plot count for unique sizes
    cc_sizes.plot(kind='bar', rot=0)

    plt.title(f'Connected components size distribution\n{name}')
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    BIG = mpatches.Patch(color='green', label='Big component')
    MEH = mpatches.Patch(color='red', label='Not big enough')
    plt.legend(handles=[BIG, MEH])

    if big_component:
        plt.gca().get_xticklabels()[-1].set_color("green")
    else:
        plt.gca().get_xticklabels()[-1].set_color("red")

    plt.xlabel('Size')
    plt.ylabel('Count')

    plt.tight_layout()

    plt.show()


def diameter_classification(graph, num_samples=20):
    # Use 2 DFS method multiple times to estimate graph diameter
    diameters = []
    for _ in range(num_samples):
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
    # test_pandas()

    real_graphs = prepare_data()
    distribution_of_connected_components(real_graphs['fb_graph'], 'Facebook Graph')
    distribution_of_connected_components(real_graphs['collaboration_network'], 'Collaboration Network')

    # graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=100, edge_prob=0.01)
    # print(f'Random graph: diameter type #{diameter_classification(graph)}.')
    # print(f'Random graph: girth type #{girth_classification(graph)}.')

    # graph = SyntheticGraphGenerator.create_grid_graph(n=10, m=21)
    # print(f'Grid graph: diameter type #{diameter_classification(graph)}.')
    # print(f'Grid graph: girth type #{girth_classification(graph)}.')


if __name__ == '__main__':
    main()
