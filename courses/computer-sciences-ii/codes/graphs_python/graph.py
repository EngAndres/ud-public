"""
This module provides a `Graph` class for creating and manipulating
unweighted, undirected graphs.

The graph is implemented using an adjacency list representation. It supports
various operations such as adding/removing vertices and edges, as well as
graph traversal algorithms like Breadth-First Search (BFS) and
Depth-First Search (DFS).
"""

from typing import Optional, Any, Dict, List, Set
from data_structures import Stack, Queue

class Graph:
    """Represents an unweighted, undirected graph."""

    def __init__(self):
        """Initializes an empty graph."""
        self.adjacency_list: Dict[Any, List[Any]] = {}
        self.vertices: Set[Any] = set()

    def add_vertex(self, new_vertex: Any):
        """Adds a new vertex to the graph.

        Args:
            new_vertex: The vertex to be added.
        """
        if new_vertex not in self.vertices:
            self.vertices.add(new_vertex)
            self.adjacency_list[new_vertex] = []
        else:
            print(f"Vertex '{new_vertex}' already exists.")

    def remove_vertex(self, vertex: Any):
        """Removes a vertex and all its associated edges from the graph.

        Args:
            vertex: The vertex to be removed.
        """
        if vertex not in self.vertices:
            print(f"Vertex '{vertex}' does not exist.")
        else:
            # Remove edges from other vertices to this one
            for neighbor in self.adjacency_list[vertex]:
                self.adjacency_list[neighbor].remove(vertex)
            # Remove the vertex itself
            del self.adjacency_list[vertex]
            self.vertices.remove(vertex)

    def add_edge(self, vertex_1: Any, vertex_2: Any):
        """Adds an edge between two vertices.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.
        """
        if vertex_1 == vertex_2:
            print("Self-loops are not allowed.")
        elif (vertex_1 not in self.vertices) or (vertex_2 not in self.vertices):
            print("Both vertices must exist in the graph to add an edge.")
        else:
            # Add edge from vertex_1 to vertex_2
            if vertex_2 not in self.adjacency_list[vertex_1]:
                self.adjacency_list[vertex_1].append(vertex_2)
            # Add edge from vertex_2 to vertex_1 (for undirected graph)
            if vertex_1 not in self.adjacency_list[vertex_2]:
                self.adjacency_list[vertex_2].append(vertex_1)

    def remove_edge(self, vertex_1: Any, vertex_2: Any):
        """Removes an edge between two vertices.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.
        """
        if (vertex_1 not in self.vertices) or (vertex_2 not in self.vertices):
            print("Both vertices must exist to remove an edge.")
        else:
            if vertex_2 in self.adjacency_list[vertex_1]:
                self.adjacency_list[vertex_1].remove(vertex_2)
            if vertex_1 in self.adjacency_list[vertex_2]:
                self.adjacency_list[vertex_2].remove(vertex_1)

    def has_edge(self, vertex_1: Any, vertex_2: Any) -> bool:
        """Checks if an edge exists between two vertices.

        Args:
            vertex_1: The first vertex.
            vertex_2: The second vertex.

        Returns:
            True if an edge exists, False otherwise.
        """
        return (vertex_1 in self.vertices and
                vertex_2 in self.adjacency_list.get(vertex_1, []))

    def get_neighbors(self, vertex: Any) -> Optional[List[Any]]:
        """Gets the list of neighbors for a given vertex.

        Args:
            vertex: The vertex whose neighbors are to be retrieved.

        Returns:
            A list of neighbors, or None if the vertex does not exist.
        """
        if vertex not in self.vertices:
            print(f"Vertex '{vertex}' does not exist.")
            return None
        return self.adjacency_list[vertex]

    def bfs(self, start: Any) -> List[Any]:
        """Performs a Breadth-First Search (BFS) traversal.

        Args:
            start: The starting vertex for the traversal.

        Returns:
            A list of vertices in BFS order.
        """
        if start not in self.vertices:
            raise ValueError(f"Start vertex '{start}' does not exist.")

        visited = set()
        queue = Queue()
        result = []

        queue.enqueue(start)
        visited.add(start)

        while not queue.is_empty():
            vertex = queue.dequeue()
            if vertex is None: continue
            result.append(vertex)

            for neighbor in self.get_neighbors(vertex) or []:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
        return result

    def dfs(self, start: Any) -> List[Any]:
        """Performs a Depth-First Search (DFS) traversal.

        Args:
            start: The starting vertex for the traversal.

        Returns:
            A list of vertices in DFS order.
        """
        if start not in self.vertices:
            raise ValueError(f"Start vertex '{start}' does not exist.")

        visited = set()
        stack = Stack()
        result = []

        stack.push(start)

        while not stack.is_empty():
            vertex = stack.pop()
            if vertex is None: continue

            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)

                # Push neighbors in reverse order to visit them in standard order
                for neighbor in sorted(self.get_neighbors(vertex) or [], reverse=True):
                    if neighbor not in visited:
                        stack.push(neighbor)
        return result

    def __str__(self) -> str:
        """Returns a string representation of the graph's adjacency list."""
        result = "Graph - Adjacency List\n"
        for vertex in sorted(self.vertices):
            neighbors = ", ".join(map(str, sorted(self.adjacency_list[vertex])))
            result += f"{vertex}: [{neighbors}]\n"
        return result
