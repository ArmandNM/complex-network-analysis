import re

from enum import Enum


class EdgeType(Enum):
    DIRECTED = 1
    UNDIRECTED = 2


class Graph:
    def __init__(self, edge_type=EdgeType.UNDIRECTED):
        self.adjacency_list = {}
        self.nodes = set()
        self.edge_type = edge_type

    @classmethod
    def create_from_edge_list(cls, file_path, header_size, edge_type=EdgeType.UNDIRECTED):
        graph = cls(edge_type)  # Construct null graph of given type

        with open(file_path, 'r') as edges_file:
            # Skip header lines
            for _ in range(header_size):
                next(edges_file)

            # Extract all edges
            edges = []
            for line in edges_file:
                src, dest = re.split(' |\t', line.strip())
                edges.append([src, dest])
                if edge_type is EdgeType.UNDIRECTED:
                    edges.append([dest, src])

        # Construct adjacency list
        for src, dest in edges:
            # Update nodes set
            graph.add_node(src)
            graph.add_node(dest)

            # Add new neighbour
            graph[src].append(dest)

        return graph

    def __getitem__(self, node):
        return self.get_neighbours(node)

    def get_neighbours(self, node):
        assert node in self.adjacency_list
        return self.adjacency_list.get(node, [])

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, src, dest):
        self.add_oriented_edge(src, dest)
        if self.edge_type == EdgeType.UNDIRECTED:
            self.add_oriented_edge(dest, src)

    def add_oriented_edge(self, src, dest):
        # Some safety checks
        assert src in self.adjacency_list
        assert src in self.nodes
        assert dest in self.nodes

        self.get_neighbours(src).append(dest)
