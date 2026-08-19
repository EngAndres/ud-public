#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_VERTICES 10

typedef struct {
    int vertices;
    int adjacencyMatrix[MAX_VERTICES][MAX_VERTICES];
} Graph;

//Operations
void initGraph(Graph *g, int newVertices){
    g->vertices = newVertices;  
    for(int i = 0; i < newVertices; i++)
        for(int j = 0; j < newVertices; j++)
            g->adjacencyMatrix[i][j] = 0;
}

/**
 * @file adjacency_matrix.c
 * @brief Implementation of a graph using an adjacency matrix.
 *
 * This file provides an implementation of a graph data structure using an
 * adjacency matrix representation. It includes functions for creating a graph,
 * adding and removing edges, and printing various matrix representations
 * of the graph.
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#define MAX_VERTICES 10

/**
 * @struct Graph
 * @brief Represents a graph using an adjacency matrix.
 *
 * @var Graph::vertices
 * Member 'vertices' represents the number of vertices in the graph.
 * @var Graph::adjacencyMatrix
 * Member 'adjacencyMatrix' is a 2D array representing the connections
 * between vertices.
 */
typedef struct {
    int vertices;
    int adjacencyMatrix[MAX_VERTICES][MAX_VERTICES];
} Graph;

// Forward declarations for function prototypes.
void initGraph(Graph *g, int newVertices);
Graph createGraph(int vertices);
void addEdge(Graph *g, int source, int destination);
bool hasEdge(Graph *g, int source, int destination);
void removeEdge(Graph *g, int source, int destination);
void printAdjacencyMatrix(Graph *g);
int countEdges(Graph *g);
void printIncidenceMatrix(Graph *g);
void printCircuitMatrix(Graph *g);
void printCutSetMatrix(Graph *g);
void printPathMatrix(Graph *g);

/**
 * @brief Initializes a graph with a given number of vertices.
 *
 * Sets the number of vertices and initializes the adjacency matrix to all zeros.
 *
 * @param g Pointer to the graph to initialize.
 * @param newVertices The number of vertices for the graph.
 */
void initGraph(Graph *g, int newVertices) {
    g->vertices = newVertices;
    for (int i = 0; i < newVertices; i++) {
        for (int j = 0; j < newVertices; j++) {
            g->adjacencyMatrix[i][j] = 0;
        }
    }
}

/**
 * @brief Creates a new graph.
 *
 * @param vertices The number of vertices in the new graph.
 * @return The newly created graph.
 */
Graph createGraph(int vertices) {
    Graph g;
    if (vertices > MAX_VERTICES) {
        puts("Error: Number of vertices exceeds the maximum allowed.\n");
        initGraph(&g, 0);
    } else {
        initGraph(&g, vertices);
    }
    return g;
}

/**
 * @brief Adds an edge between two vertices.
 *
 * For an undirected graph, this function sets the corresponding entries in the
 * adjacency matrix to 1.
 *
 * @param g Pointer to the graph.
 * @param source The source vertex.
 * @param destination The destination vertex.
 */
void addEdge(Graph *g, int source, int destination) {
    if (source == destination) {
        puts("Self-loops are not allowed.\n");
        return;
    }
    if (source < g->vertices && destination < g->vertices) {
        g->adjacencyMatrix[source][destination] = 1;
        g->adjacencyMatrix[destination][source] = 1; // For undirected graph.
    } else {
        puts("Error: Vertex out of bounds.\n");
    }
}

/**
 * @brief Checks if an edge exists between two vertices.
 *
 * @param g Pointer to the graph.
 * @param source The source vertex.
 * @param destination The destination vertex.
 * @return True if an edge exists, false otherwise.
 */
bool hasEdge(Graph *g, int source, int destination) {
    if (source < g->vertices && destination < g->vertices) {
        return g->adjacencyMatrix[source][destination] == 1;
    }
    puts("Error: Vertex out of bounds.\n");
    return false;
}

/**
 * @brief Removes an edge between two vertices.
 *
 * @param g Pointer to the graph.
 * @param source The source vertex.
 * @param destination The destination vertex.
 */
void removeEdge(Graph *g, int source, int destination) {
    if (hasEdge(g, source, destination)) {
        g->adjacencyMatrix[source][destination] = 0;
        g->adjacencyMatrix[destination][source] = 0; // For undirected graph.
    } else {
        puts("Edge does not exist.\n");
    }
}

/**
 * @brief Prints the adjacency matrix of the graph.
 *
 * @param g Pointer to the graph.
 */
void printAdjacencyMatrix(Graph *g) {
    printf("==== ADJACENCY MATRIX ====");
    printf("\t");
    for (int i = 0; i < g->vertices; i++) {
        printf("[%d]\t", i);
    }
    printf("\n");

    for (int i = 0; i < g->vertices; i++) {
        printf("[%d]\t", i);
        for (int j = 0; j < g->vertices; j++) {
            printf("%d\t", g->adjacencyMatrix[i][j]);
        }
        printf("\n");
    }
}

/**
 * @brief Main function to demonstrate graph operations.
 *
 * Creates a graph, adds edges, and prints its adjacency matrix.
 *
 * @return 0 on successful execution.
 */
int main() {
    Graph myGraph = createGraph(5);

    addEdge(&myGraph, 0, 1);
    addEdge(&myGraph, 0, 4);
    addEdge(&myGraph, 1, 2);
    addEdge(&myGraph, 1, 3);
    addEdge(&myGraph, 1, 4);
    addEdge(&myGraph, 2, 3);
    addEdge(&myGraph, 3, 4);

    printAdjacencyMatrix(&myGraph);

    // Example of other matrix representations (if implemented).
    // printIncidenceMatrix(&myGraph);
    // printCircuitMatrix(&myGraph);
    // printCutSetMatrix(&myGraph);
    // printPathMatrix(&myGraph);

    return 0;
}

void addEdge(Graph *g, int source, int destination){
    if(source == destination){
        puts("El origen y el destino no pueden ser iguales.\n");
        return;
    }
    if(source < g->vertices && destination < g->vertices){
        g->adjacencyMatrix[source][destination] = 1;
        g->adjacencyMatrix[destination][source] = 1; //remove in directed graph
    } else {
        puts("El origen o el destino no corresponden a los nodos definidos en el grafo.\n");
        return;
    }
}

bool hasEdge(Graph *g, int source, int destination){
    bool has = false;
    if(source < g->vertices && destination < g->vertices){
        if(g->adjacencyMatrix[source][destination] == 1){
            has = true;
        }
    } else {
        puts("El origen o el destino no corresponden a los nodos definidos en el grafo.\n");
        return false;
    }
    return has;
}

void removeEdge(Graph *g, int source, int destination){
    if(hasEdge(g, source, destination)){
        g->adjacencyMatrix[source][destination] = 0;
        g->adjacencyMatrix[destination][source] = 0;
    } else {
        puts("No se puede eliminar la arista entre los nodos definidos.");
    }
}

void printAdjacencyMatrix(Graph *g){
    printf("====GRAPH=====");
    //printf("\t");
    for(int i = 0; i < g->vertices; i++)
        printf("\t[%d]", i); // header
    printf("\n");

    for(int i = 0; i < g->vertices; i++){
        printf("\t[%d]", i);
        for(int j = 0; j < g->vertices; j++)
            printf("%d", g->adjacencyMatrix[i][j]);
        printf("\n");
    }
}

int countEdges(Graph *g){
    int edgeCount = 0;
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < i; j++)
            if(g->adjacencyMatrix[i][j] == 1)
                edgeCount++;
    return edgeCount;
}

void printIncidenceMatrix(Graph *g){
    printf("\n=====INCIDENCE MATRIX=====");

    int edgeCount = countEdges(g);
    if(edgeCount == 0){
        printf("No hay aristas en el grafo.");
        return;
    }    

    int incidenceMatrix[g->vertices][edgeCount];
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < edgeCount; j++)
            incidenceMatrix[i][j] = 0;

    int edgeIndex = 0;
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < i; j++)
            if(g->adjacencyMatrix[i][j] == 1){
                incidenceMatrix[i][edgeIndex] = 1; //source
                incidenceMatrix[j][edgeIndex] = 1; //destination
                edgeIndex++;
            }

    for(int i = 0; i < edgeCount; i++)
        printf("\t[%d]", i); // header
    printf("\n");

    for(int i = 0; i < g->vertices; i++){
        printf("\t[%d]", i);
        for(int j = 0; j < edgeCount; j++)
            printf("%d", incidenceMatrix[i][j]);
        printf("\n");
    }
}

int getEdgeList(Graph *g){
    int edgeCount = countEdges(g);
    int edgeList[edgeCount][2];
    int edgeIndex = 0;
    for(int i = 0; i < g->vertices && edgeIndex < edgeCount; i++)
        for(int j = 0; j < g->vertices && edgeIndex < edgeCount; j++)
            if(g->adjacencyMatrix[i][j] == 1){
                edgeList[edgeIndex][0] = i; //source
                edgeList[edgeIndex][1] = j; //destination
            }
    return edgeList;
}
    
void printCircuitMatrix(Graph *g){
    printf("\n=====CIRCUIT MATRIX (Back Edges)=====\n");
    int edgeCount = countEdges(g);
    if(edgeCount == 0){
        printf("No hay aristas en el grafo.\n");
        return;
    }

    int cycles = edgeCount - g->vertices + 1;
    if(cycles <= 0){
        printf("No hay ciclos fundamentales.\n");
        return;
    }

    int **circuit = (int **)malloc(cycles * sizeof(int *));
    for(int i = 0; i < cycles; i++)
        circuit[i] = (int *)malloc(edgeCount * sizeof(int));

    // Initialize to 0
    for(int i = 0; i < cycles; i++)
        for(int j = 0; j < edgeCount; j++)
            circuit[i][j] = 0;

    // Build edge list
    int edgeList[edgeCount][2];
    int idx = 0;
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < i; j++)
            if(g->adjacencyMatrix[i][j] == 1){
                edgeList[idx][0] = i;
                edgeList[idx][1] = j;
                idx++;
            }

    // Find back edges using simple cycle detection
    int cycleIndex = 0;
    for(int e1 = 0; e1 < edgeCount && cycleIndex < cycles; e1++){
        int v1 = edgeList[e1][0];
        int v2 = edgeList[e1][1];
        
        // Mark this edge
        circuit[cycleIndex][e1] = 1;
        
        // Find path from v2 to v1 using other edges
        for(int e2 = 0; e2 < edgeCount; e2++){
            if(e2 != e1){
                int u1 = edgeList[e2][0];
                int u2 = edgeList[e2][1];
                // Simple heuristic: mark adjacent edges
                if((v1 == u1 || v1 == u2 || v2 == u1 || v2 == u2)){
                    circuit[cycleIndex][e2] = 1;
                }
            }
        }
        cycleIndex++;
    }

    // Print header
    printf("   ");
    for(int i = 0; i < edgeCount; i++)
        printf("\te%d", i);
    printf("\n");

    // Print matrix
    for(int i = 0; i < cycles; i++){
        printf("c%d\t", i);
        for(int j = 0; j < edgeCount; j++)
            printf("%d\t", circuit[i][j]);
        printf("\n");
    }

    // Free memory
    for(int i = 0; i < cycles; i++)
        free(circuit[i]);
    free(circuit);
}

void printCutSetMatrix(Graph *g){
    printf("\n=====CUT-SET MATRIX (Edges by Vertex Partition)=====\n");
    int edgeCount = countEdges(g);
    if(edgeCount == 0) {
        printf("No hay aristas en el grafo.\n");
        return;
    }

    int cutsets = g->vertices - 1;
    int **cutset = (int **)malloc(cutsets * sizeof(int *));
    for(int i = 0; i < cutsets; i++)
        cutset[i] = (int *)malloc(edgeCount * sizeof(int));

    // Initialize to 0
    for(int i = 0; i < cutsets; i++)
        for(int j = 0; j < edgeCount; j++)
            cutset[i][j] = 0;

    // Build edge list
    int edgeList[edgeCount][2];
    int idx = 0;
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < i; j++)
            if(g->adjacencyMatrix[i][j] == 1){
                edgeList[idx][0] = i;
                edgeList[idx][1] = j;
                idx++;
            }

    // Classic approach: partition vertices at each cut point
    for(int partition = 0; partition < cutsets; partition++){
        for(int e = 0; e < edgeCount; e++){
            int v1 = edgeList[e][0];
            int v2 = edgeList[e][1];
            // Mark edges that cross partition boundaries
            // Partition: vertices <= partition on one side, > partition on other
            if((v1 <= partition && v2 > partition) || 
               (v2 <= partition && v1 > partition)){
                cutset[partition][e] = 1;
            }
        }
    }

    // Print header
    printf("   ");
    for(int i = 0; i < edgeCount; i++)
        printf("\te%d", i);
    printf("\n");

    // Print matrix
    for(int i = 0; i < cutsets; i++){
        printf("s%d\t", i);
        for(int j = 0; j < edgeCount; j++)
            printf("%d\t", cutset[i][j]);
        printf("\n");
    }

    // Free memory
    for(int i = 0; i < cutsets; i++)
        free(cutset[i]);
    free(cutset);
}

void printPathMatrix(Graph *g){
    printf("\n======PATH MATRIX=====\n");
    int pathMatrix[g->vertices][g->vertices];
    for(int i = 0; i < g->vertices; i++)
        for(int j = 0; j < g->vertices; j++)
            if(i == j)
                pathMatrix[i][j] = 1;
            else
                pathMatrix[i][j] = g->adjacencyMatrix[i][j];
    
    // Algorithm: Floyd-Warshall
    for(int k = 0; k < g->vertices; k++)
        for(int i = 0; i < g->vertices; i++)
            for(int j = 0; j < g->vertices; j++)
                if(pathMatrix[i][k] && pathMatrix[k][j])
                    pathMatrix[i][j] = 1;

    for(int i = 0; i < g->vertices; i++)
        printf("\t[%d]", i); // header
    printf("\n");

    for(int i = 0; i < g->vertices; i++){
        printf("\t[%d]", i);
        for(int j = 0; j < g->vertices; j++)
            printf("%d", pathMatrix[i][j]);
        printf("\n");
    }
}

int main(){
    int vertices;
    printf("Ingrese cantidad de vertices: ");
    scanf("%d", &vertices);
    Graph graph = createGraph(vertices);



    return 0;
}