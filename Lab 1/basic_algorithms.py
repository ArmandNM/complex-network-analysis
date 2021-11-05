import pprint

from queue import Queue

from synthetic_data import SyntheticGraphGenerator


def depth_first_search(graph, starting_node):
    def _dfs(crt_node, graph, visited, output):
        visited.add(crt_node)
        output.append(crt_node)

        for neigh in graph.get_neighbours(crt_node):
            if neigh not in visited:
                _dfs(neigh, graph, visited, output)

    visited = set()  # no nodes yet visited
    output = []  # order of visiting nodes

    _dfs(starting_node, graph, visited, output)

    return visited, output


def breadth_first_search(graph, starting_node):
    visited = set()  # no nodes yet visited
    output = []  # order of visiting nodes
    q = Queue()

    q.put(starting_node)
    visited.add(starting_node)

    while not q.empty():
        node = q.get()
        output.append(node)

        for neigh in graph.get_neighbours(node):
            if neigh not in visited:
                visited.add(neigh)
                q.put(neigh)

    return visited, output


def get_connected_components(graph):
    pass


def compute_degree_sequence(graph):
    pass


def compute_diameter(graph):
    pass


def compute_girth(graph):
    pass


def main():
    pp = pprint.PrettyPrinter(indent=4)

    random_graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=5, edge_prob=0.5)
    pp.pprint(random_graph.adjacency_list)

    _, out = depth_first_search(random_graph, next(iter(random_graph.nodes)))
    print(out)

    _, out = breadth_first_search(random_graph, next(iter(random_graph.nodes)))
    print(out)


if __name__ == '__main__':
    main()
