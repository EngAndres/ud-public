from typing import Optional, Any, Dict, List, Set
from data_structures import Stack, Queue

class Graph:

    def __init__(self):
        self.adjancency_list: Dict[Any, List[Any]] = {}
        self.vertices: Set[Any] = set()

    def add_vertex(self, new_vertex: Any):
        if new_vertex not in self.vertices:
            self.vertices.add( new_vertex )
            self.adjancency_list[new_vertex] = []
        else:
            print("El vertice ya existe.")

    def remove_vertex(self, vertex: Any):
        if vertex not in self.vertices:
            print("No existe el vertice que se quiere eliminar.")
        else:
            for neighbor in self.adjancency_list[vertex]:
                self.adjancency_list[neighbor].remove(vertex)
            del self.adjancency_list[vertex]
            self.vertices.remove(vertex)

    def add_edge(self, vertex_1: Any, vertex_2: Any):
        if vertex_1 == vertex_2:
            print("No se admiten bucles al mismo nodo.")
        else:
            if (vertex_1 not in self.vertices) or (vertex_2 not in self.vertices):
                print("Colocar vertices que existan en el grafo.")
            else:
                if vertex_2 not in self.adjancency_list[vertex_1]:
                    self.adjancency_list[vertex_1].append(vertex_2)
                if vertex_1 not in self.adjancency_list[vertex_2]:
                    self.adjancency_list[vertex_2].append(vertex_1)
                

    def remove_edge(self, vertex_1: Any, vertex_2: Any):
        if (vertex_1 not in self.vertices) or (vertex_2 not in self.vertices):
            print("No se puede eliminar una arista de nodos que no existen.")
        else:
            if vertex_2 in self.adjancency_list[vertex_1]:
                self.adjancency_list[vertex_1].remove(vertex_2)
            if vertex_1 in self.adjancency_list[vertex_2]:
                self.adjancency_list[vertex_2].remove(vertex_1)

    def has_edge(self, vertex_1: Any, vertex_2: Any):
        if (vertex_2 in self.adjancency_list[vertex_1]) and \
            (vertex_1 in self.adjancency_list[vertex_2]):
            return True
        return False
    

    def get_neighbors(self, vertex: Any) -> Optional[List[Any]]:
        if vertex not in self.vertices:
            print(f'El nodo {vertex} no existe en el grafo.')
            return None
        return self.adjancency_list[vertex]
    
    def bfs(self, start: Any) -> List[Any]:
        if start not in self.vertices:
            raise ValueError(f'El vertice {start} no existe.')

        visited = set()
        queue = Queue()
        result = []

        queue.enqueue(start)
        visited.add(start)

        while not queue.is_empty():
            vertex = queue.dequeue()
            result.appen(vertex)
        
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(visited)
                    queue.enqueue(neighbor)
        
        return result
    
    def bfs_targe(self, start: Any, target: Any) -> List[Any]:
        if start not in self.vertices:
            raise ValueError(f'El vertice {start} no existe.')

        visited = set()
        queue = Queue()
        result = []

        queue.enqueue(start)
        visited.add(start)

        while not queue.is_empty():
            vertex = queue.dequeue()
            result.appen(vertex)

            if target == vertex:
                break
        
            for neighbor in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(visited)
                    queue.enqueue(neighbor)
        
        return result
    
    def dfs(self, start: Any) -> List[Any]:
        if start not in self.vertices:
            raise ValueError(f'El vertice {start} no existe')

        visited = set()
        stack = Stack()
        result = []

        stack.push(start)
        visited.add(start)

        while not stack.is_empty():
            vertex = stack.pop()
            result.append(vertex)

            for neighbor in reversed(self.adjancency_list[vertex]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.push(neighbor)
        
        return result