"""
This module provides basic data structures like Node, LinkedList, Stack, and Queue.

These data structures are fundamental for implementing more complex algorithms
and are used throughout this project, particularly in graph traversal.
"""

from typing import Any, Optional, List

class Node:
    """Represents a single node in a linked list."""

    def __init__(self, new_data: Any):
        """Initializes a new Node.

        Args:
            new_data: The data to be stored in the node.
        """
        self.data = new_data
        self.next: Optional['Node'] = None

class LinkedList:
    """A singly linked list implementation."""

    def __init__(self):
        """Initializes an empty linked list."""
        self.head: Optional[Node] = None
        self.size: int = 0

    def _append(self, data: Any):
        """Adds a new node with data to the end of the list.

        Args:
            data: The data to append.
        """
        new_node = Node(data)
        if not self.head:  # If the list is empty
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            # current is now the last node
            current.next = new_node
        self.size += 1

    def _prepend(self, data: Any):
        """Adds a new node with data to the beginning of the list.

        Args:
            data: The data to prepend.
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def _remove_and_return(self, position: str) -> Optional[Any]:
        """Removes and returns a node from the specified position.

        Args:
            position: 'begin' or 'end' to specify which node to remove.

        Returns:
            The data of the removed node, or None if the list is empty or
            the position is invalid.
        """
        if not self.head:
            print("Cannot remove an element from an empty list.")
            return None

        if not self.head.next:
            # List with only one item
            value = self.head.data
            self.head = None
        elif position == 'end':
            current = self.head
            while current.next and current.next.next:
                current = current.next
            # current is the second to last node
            value = current.next.data
            current.next = None
        elif position == "begin":
            value = self.head.data
            self.head = self.head.next
        else:
            print("Invalid position for deletion.")
            return None

        self.size -= 1
        return value

    def to_list(self) -> List[Any]:
        """Converts the linked list to a Python list.

        Returns:
            A list containing the data of all nodes in the linked list.
        """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self) -> bool:
        """Checks if the linked list is empty.

        Returns:
            True if the list is empty, False otherwise.
        """
        return self.head is None

    def __len__(self) -> int:
        """Returns the number of nodes in the list."""
        return self.size

    def __iter__(self):
        """Provides an iterator for the linked list."""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self) -> str:
        """Returns a string representation of the linked list.

        Returns:
            A comma-separated string of the list's elements.
        """
        return ', '.join(map(str, self.to_list()))


class Stack(LinkedList):
    """A stack data structure, implemented using a linked list (LIFO)."""

    def push(self, data: Any):
        """Adds an element to the top of the stack.

        Args:
            data: The data to push onto the stack.
        """
        self._prepend(data)

    def pop(self) -> Optional[Any]:
        """Removes and returns the element from the top of the stack.

        Returns:
            The data from the top of the stack, or None if the stack is empty.
        """
        return self._remove_and_return('begin')


class Queue(LinkedList):
    """A queue data structure, implemented using a linked list (FIFO)."""

    def enqueue(self, data: Any):
        """Adds an element to the end of the queue.

        Args:
            data: The data to add to the queue.
        """
        self._append(data)

    def dequeue(self) -> Optional[Any]:
        """Removes and returns the element from the front of the queue.

        Returns:
            The data from the front of the queue, or None if the queue is empty.
        """
        return self._remove_and_return('begin')
    