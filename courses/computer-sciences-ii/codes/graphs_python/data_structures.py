from typing import Any, Optional, List

class Node:
    def __init__(self, new_data: Any):
        """Class constructor"""
        self.data = new_data
        self.next: Optional['Node'] = None

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self.size: int = 0

    def _append(self, data: Any):
        """Add to the end"""
        new_node = Node(data)
        if not self.head: # empty list
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            # here current should be the last
            current.next = new_node
        
        self.size += 1

    def _prepend(self, data: Any):
        """Insert to the beginning"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def _remove_and_return(self, position: str):
        if not self.head:
            print("No se puede remover un elemento en una lista vacia.")
            return None
        
        if not self.head.next:
            # list of one item
            value = self.head.data
            self.head = None
        
        if position == 'end':
            current = self.head
            while current.next.next:
                current = current.next
            #current is penultimate
            value = current.next.data 
            current.next = None
        elif position == "begin":
            value = self.head.data
            self.head = self.head.next
        else:
            print("Posicion incorrecta para borrar.")
            return None
        
        self.size -= 1
        return value
    
    def to_list(self) -> List[Any]:
        result = []
        current = self.head
        while current:
            result.append( current.data );
            current = current.next
        return result
    
    def is_empty(self) -> bool:
        return self.head
    
    def __len__(self) -> int:
        return self.size
    
    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
        
    def __str__(self) -> str:
        return ', '.join(self.to_list())


class Stack(LinkedList):

    def push(self, data: Any):
        self._prepend(data)

    def pop(self) -> Optional[Any]:
        return self._remove_and_return('begin')
    


class Queue(LinkedList):

    def enqueue(self, data: Any):
        self._append(data)
    
    def dequeue(self) -> Optional[Any]:
        return self._remove_and_return('begin')
    