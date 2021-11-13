import pprint

from synthetic_data import SyntheticGraphGenerator


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


def main():
    pp = pprint.PrettyPrinter(indent=4)

    graph = SyntheticGraphGenerator.create_random_edge_graph(num_nodes=5, edge_prob=0.5)
    pp.pprint(graph.adjacency_list)
    print(f'Random graph: num_traingles = {count_triangles(graph)}')


if __name__ == '__main__':
    main()
