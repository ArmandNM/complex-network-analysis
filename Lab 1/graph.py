import re

from enum import Enum


class EdgeType(Enum):
    DIRECTED = 1
    UNDIRECTED = 2


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    @classmethod
    def create_from_edge_list(cls, file_path, header_size, edge_type=EdgeType.UNDIRECTED):
        graph = cls()

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
            if src not in graph.adjacency_list:
                graph.adjacency_list[src] = []
            graph[src].append(dest)

        return graph

    def __getitem__(self, node_id):
        return self.get_neighbours(node_id)

    def get_neighbours(self, node_id):
        return self.adjacency_list.get(node_id, [])
