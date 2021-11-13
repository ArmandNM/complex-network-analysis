import pprint
import numpy as np
import random

from queue import Queue

from graph import EdgeType, Graph
from synthetic_data import SyntheticGraphGenerator


def depth_first_search(graph, starting_node):
    def _dfs(crt_node, graph, visited, output):
        visited.add(crt_node)
        output.append(crt_node)

        for neigh in graph.get_neighbours(crt_node):
            if neigh not in visited:
                _dfs(neigh, graph, visited, output)

    visited = set()  # No nodes yet visited
    output = []  # Order of visiting nodes

    _dfs(starting_node, graph, visited, output)

    return visited, output


def breadth_first_search(graph, starting_node):
    visited = set()  # No nodes yet visited
    output = []  # Order of visiting nodes
    q = Queue()

    q.put([starting_node, 0])  # [node, distance]
    visited.add(starting_node)

    while not q.empty():
        node, distance = q.get()
        output.append([node, distance])

        for neigh in graph.get_neighbours(node):
            if neigh not in visited:
                visited.add(neigh)
                q.put([neigh, distance + 1])

    return visited, output


def get_connected_components(graph):
    components = []
    visited = set()

    for node in graph.nodes:
        if node not in visited:
            component, _ = depth_first_search(graph, node)
            components.append(component)
            visited.update(component)

    return components


def compute_degree_sequence(graph):
    in_degree = {}
    out_degree = {}

    for node in graph.nodes:
        in_degree[node] = 0
        out_degree[node] = 0

    for node in graph.nodes:
        for neigh in graph.get_neighbours(node):
            in_degree[neigh] += 1
            out_degree[node] += 1

    degree = {}
    for node in graph.nodes:
        if graph.edge_type == EdgeType.UNDIRECTED:
            degree[node] = out_degree[node]  # same as in_degree
        elif graph.edge_type == EdgeType.DIRECTED:
            degree[node] = (in_degree[node], out_degree[node])

    return degree


def compute_diameter(graph, start_node='first'):  # start_node = 'first' or 'random'
    assert start_node in ['first', 'random']

    if start_node == 'first':
        start_node = next(iter(graph.nodes))
    elif start_node == 'random':
        start_node = random.choice(list(graph.nodes))

    # Run BFS from arbitrary node
    _, out = breadth_first_search(graph, next(iter(graph.nodes)))

    # Check if graph is connected
    if len(out) < len(graph.nodes):
        return np.inf, None, None

    # Get farthest node from first traversal
    src, _ = max(out, key=lambda o: o[1])

    # Get farthest distance from second traversal
    _, out = breadth_first_search(graph, src)
    dest, diameter = max(out, key=lambda o: o[1])

    return diameter, src, dest


def compute_girth(graph):
    def _bfs(starting_node, graph):
        shortest_cycle = np.inf  # + [optional] tail

        visited = set()  # No nodes yet visited
        node_dist = {}
        q = Queue()

        q.put([starting_node, 0])  # [node, distance]
        node_dist[starting_node] = 0
        visited.add(starting_node)

        while not q.empty():
            node, distance = q.get()

            for neigh in graph.get_neighbours(node):
                if neigh in visited:
                    neigh_dist = node_dist[neigh]
                    if neigh_dist < distance:
                        continue  # era ta-su mă

                    if neigh_dist == distance:
                        shortest_cycle = 2 * neigh_dist + 1
                    elif neigh_dist == distance + 1:
                        shortest_cycle = 2 * neigh_dist

                    return shortest_cycle

                if neigh not in visited:
                    visited.add(neigh)
                    node_dist[neigh] = distance + 1
                    q.put([neigh, distance + 1])

        return shortest_cycle

    girth = np.inf

    for node in graph.nodes:
        shortest_cycle = _bfs(node, graph)
        girth = min(girth, shortest_cycle)

    return girth


def main():
    pp = pprint.PrettyPrinter(indent=4)

    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=10, edge_prob=0.1)
    print('Random graph:')
    pp.pprint(random_graph.adjacency_list)

    _, out = depth_first_search(random_graph, next(iter(random_graph.nodes)))
    print('DFS:', out)

    _, out = breadth_first_search(random_graph, next(iter(random_graph.nodes)))
    print('BFS:', out)

    cc = get_connected_components(random_graph)
    print('Connected components:')
    pp.pprint(cc)

    degree_sequence = compute_degree_sequence(random_graph)
    print('Degree sequence:')
    pp.pprint(degree_sequence)

    diameter, src, dest = compute_diameter(random_graph)
    print(f'Diameter: {diameter} between nodes {src} and {dest}.')

    girth = compute_girth(random_graph)
    print(f'Girth random graph: {girth}.')
    custom_graph = Graph()
    custom_graph.add_node(1)
    custom_graph.add_node(2)
    custom_graph.add_node(3)
    custom_graph.add_node(4)
    custom_graph.add_node(5)
    custom_graph.add_edge(1, 2)
    custom_graph.add_edge(2, 3)
    custom_graph.add_edge(3, 4)
    custom_graph.add_edge(4, 5)
    custom_graph.add_edge(5, 1)
    girth = compute_girth(custom_graph)
    print(f'Girth custom graph: {girth}.')

    custom_graph2 = Graph()
    custom_graph2.nodes = set(range(10))
    custom_graph2.adjacency_list = {
        0: [1, 7],
        1: [0, 2, 3, 4, 5, 6, 8, 9],
        2: [1, 3, 4, 5, 6, 8, 9],
        3: [1, 2, 4, 7, 9],
        4: [1, 2, 3, 5, 6, 9],
        5: [1, 2, 4, 6, 8, 9],
        6: [1, 2, 4, 5, 7],
        7: [0, 3, 6, 9],
        8: [1, 2, 5],
        9: [1, 2, 3, 4, 5, 7]
    }
    girth = compute_girth(custom_graph2)
    print(f'Girth custom graph2: {girth}.')

    grid_graph = SyntheticGraphGenerator.create_grid_graph(3, 4)
    girth = compute_girth(grid_graph)
    print(f'Girth grid graph: {girth}.')


if __name__ == '__main__':
    main()
