"""
This module provides a `WeightedGraph` class for creating and manipulating
weighted, undirected graphs.

The graph is implemented using an adjacency list, where each entry stores a
tuple of a neighbor and the weight of the edge. It supports operations like
adding/removing vertices and weighted edges.
"""

from typing import Any, List, Dict, Optional, Tuple, Set

class WeightedGraph:
    """Represents a weighted, undirected graph."""

    def __init__(self):
        """Initializes an empty weighted graph."""
        self.adjacency_list: Dict[Any, List[Tuple[Any, float]]] = {}
        self.vertices: Set[Any] = set()
        # Using a set for edges to avoid duplicates and store weights.
        # The format is (vertex1, vertex2, weight) where vertex1 < vertex2.
        self.edges: Set[Tuple[Any, Any, float]] = set()

    def add_vertex(self, vertex: Any):
        """Adds a new vertex to the graph.

        Args:
            vertex: The vertex to be added.
        """
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.adjacency_list[vertex] = []
        else:
            print(f"Vertex '{vertex}' already exists in the graph.")

    def remove_vertex(self, vertex: Any):
        """Removes a vertex and all its associated edges from the graph.

        Args:
            vertex: The vertex to be removed.
        """
        if vertex in self.vertices:
            # Remove edges from other vertices to this one.
            for neighbor, _ in self.adjacency_list[vertex]:
                self.adjacency_list[neighbor] = [
                    (v, w) for v, w in self.adjacency_list[neighbor] if v != vertex
                ]
            # Remove the vertex itself from the adjacency list and vertex set.
            del self.adjacency_list[vertex]
            self.vertices.remove(vertex)
            # Remove all edges connected to this vertex from the edges set.
            self.edges = {
                (v1, v2, w) for v1, v2, w in self.edges if v1 != vertex and v2 != vertex
            }
        else:
            print(f"Vertex '{vertex}' does not exist in the graph.")

    def add_weighted_edge(self, vertex_1: Any, vertex_2: Any, weight: float):
        """Adds a weighted edge between two vertices.

        If an edge already exists, its weight is updated.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.
            weight: The weight of the edge. Must be non-negative.
        """
        if vertex_1 == vertex_2:
            print("Self-loops are not allowed.")
            return
        if weight < 0.0:
            print("Edge weight must be non-negative.")
            return
        if vertex_1 not in self.vertices or vertex_2 not in self.vertices:
            print("Both vertices must exist in the graph.")
            return

        # Ensure consistent ordering of vertices in the edge tuple.
        v1, v2 = min(vertex_1, vertex_2), max(vertex_1, vertex_2)

        # Remove any existing edge to update it.
        self.remove_weighted_edge(v1, v2)

        # Add the new edge to the adjacency lists.
        self.adjacency_list[vertex_1].append((vertex_2, weight))
        self.adjacency_list[vertex_2].append((vertex_1, weight))

        # Add the edge to the set of edges.
        self.edges.add((v1, v2, weight))

    def has_edge(self, vertex_1: Any, vertex_2: Any) -> bool:
        """Checks if an edge exists between two vertices.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.

        Returns:
            True if an edge exists, False otherwise.
        """
        if vertex_1 not in self.vertices or vertex_2 not in self.vertices:
            print("Both vertices must exist in the graph.")
            return False
        
        v1, v2 = min(vertex_1, vertex_2), max(vertex_1, vertex_2)
        return any(e[0] == v1 and e[1] == v2 for e in self.edges)

    def remove_weighted_edge(self, vertex_1: Any, vertex_2: Any):
        """Removes a weighted edge between two vertices.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.
        """
        if vertex_1 not in self.vertices or vertex_2 not in self.vertices:
            print("Both vertices must exist in the graph.")
            return

        if self.has_edge(vertex_1, vertex_2):
            # Remove from adjacency lists.
            self.adjacency_list[vertex_1] = [
                (v, w) for v, w in self.adjacency_list[vertex_1] if v != vertex_2
            ]
            self.adjacency_list[vertex_2] = [
                (v, w) for v, w in self.adjacency_list[vertex_2] if v != vertex_1
            ]

            # Remove from the set of edges.
            v1, v2 = min(vertex_1, vertex_2), max(vertex_1, vertex_2)
            self.edges = {
                (e_v1, e_v2, w) for e_v1, e_v2, w in self.edges if not (e_v1 == v1 and e_v2 == v2)
            }
        else:
            print("No edge exists between the specified vertices.")

    def __str__(self) -> str:
        """Returns a string representation of the weighted graph."""
        result = "Weighted Graph - Adjacency List\n"
        for vertex in sorted(self.vertices):
            neighbors = ", ".join(f"({n}, {w})" for n, w in sorted(self.adjacency_list[vertex]))
            result += f"{vertex}: [{neighbors}]\n"
        return result