import pprint
import numpy as np

from queue import Queue

from graph import EdgeType
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


def compute_diameter(graph):
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
    pass


def main():
    pp = pprint.PrettyPrinter(indent=4)

    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=5, edge_prob=0.5)
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


if __name__ == '__main__':
    main()
