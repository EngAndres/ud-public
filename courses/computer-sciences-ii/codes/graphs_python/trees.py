"""
This module provides a `Tree` class, which is a specialized form of a `Graph`.

The `Tree` class inherits from `Graph` and includes methods specific to
tree data structures, such as finding the parent of a node, calculating
node depth and height, and identifying the lowest common ancestor.
"""

from typing import Optional, Any, List, Dict
from data_structures import Queue
from graph import Graph

class Tree(Graph):
    """Represents a tree data structure, inheriting from Graph."""

    def __init__(self, root: Optional[Any] = None):
        """Initializes a new Tree.

        Args:
            root: The root node of the tree. Defaults to None.
        """
        super().__init__()
        self.root = root
        if self.root is not None:
            self.add_vertex(self.root)

    def set_root(self, root: Any):
        """Sets the root of the tree.

        Args:
            root: The node to be set as the new root.
        """
        if root not in self.vertices:
            print(f"Node '{root}' does not exist in the tree.")
        else:
            self.root = root

    def get_parent(self, node: Any) -> Optional[Any]:
        """Finds the parent of a given node in the tree.

        This method performs a BFS traversal starting from the root to find
        the node that has the given node as a child.

        Args:
            node: The node whose parent is to be found.

        Returns:
            The parent node, or None if the node is the root or does not exist.
        """
        if node not in self.vertices:
            print(f"Node '{node}' does not exist.")
            return None
        if self.is_empty() or node == self.root:
            return None

        # BFS to find the parent
        queue = Queue()
        queue.enqueue(self.root)
        visited = {self.root}

        while not queue.is_empty():
            current_node = queue.dequeue()
            if current_node is None: continue

            for neighbor in self.get_neighbors(current_node) or []:
                if neighbor == node:
                    return current_node
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
        return None

    def get_children(self, node: Any) -> List[Any]:
        """Gets the children of a given node.

        Args:
            node: The node whose children are to be retrieved.

        Returns:
            A list of child nodes.
        """
        if node not in self.vertices or self.is_empty():
            return []

        neighbors = self.get_neighbors(node) or []
        parent = self.get_parent(node)
        # Children are all neighbors except the parent.
        if parent is None: # It's the root
            return neighbors
        return [n for n in neighbors if n != parent]

    def get_path(self, start: Any, end: Any) -> List[Any]:
        """Finds the path from a starting node to an end node.

        Args:
            start: The starting node of the path.
            end: The ending node of the path.

        Returns:
            A list of nodes representing the path from start to end.
        """
        if start not in self.vertices or end not in self.vertices:
            print("Start or end node does not exist in the tree.")
            return []

        # BFS to find the path and keep track of parents.
        parent_map = {start: None}
        queue = Queue()
        queue.enqueue(start)
        visited = {start}

        path_found = False
        while not queue.is_empty():
            node = queue.dequeue()
            if node is None: continue

            if node == end:
                path_found = True
                break

            for neighbor in self.get_neighbors(node) or []:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent_map[neighbor] = node
                    queue.enqueue(neighbor)
        
        if not path_found:
            return []

        # Reconstruct the path from end to start.
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent_map.get(current)
        return path[::-1]  # Reverse to get path from start to end.

    def is_empty(self) -> bool:
        """Checks if the tree is empty.

        Returns:
            True if the tree has no root, False otherwise.
        """
        return self.root is None

    def lowest_common_ancestor(self, node_1: Any, node_2: Any) -> Optional[Any]:
        """Finds the lowest common ancestor (LCA) of two nodes.

        Args:
            node_1: The first node.
            node_2: The second node.

        Returns:
            The lowest common ancestor node, or None if not found.
        """
        if (node_1 not in self.vertices) or (node_2 not in self.vertices):
            print("Both nodes must exist in the tree.")
            return None
        
        path_1 = self.get_path(self.root, node_1)
        path_2 = self.get_path(self.root, node_2)

        if not path_1 or not path_2:
            print("Could not find a path to one or both nodes from the root.")
            return None
        
        lca = None
        for anc_1, anc_2 in zip(path_1, path_2):
            if anc_1 == anc_2:
                lca = anc_1
            else:
                break
        return lca

    def __str__(self) -> str:
        """Returns a string representation of the tree."""
        if self.is_empty():
            return "Tree is empty."
        result = f"Tree (Root: {self.root})\n"
        result += super().__str__()
        return result



