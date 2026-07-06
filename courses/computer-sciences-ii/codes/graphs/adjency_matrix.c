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

Graph createGraph(int vertices){
    Graph g;
    if(vertices > MAX_VERTICES){
        puts("Cantidad de vertices superior a la permitida.\n");
        exit(EXIT_FAILURE);
    }
    initGraph(&g, vertices);
    return g;
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
        return;
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
    prinft("\n======PRINT CIRCUIT MATRIX=====");
    int edgeCount = countEdges(g);
    if(edgeCount == 0){
        printf("No hay aristas en el grafo.");
        return;
    }

    int cycles = edgeCount - g->vertices;
    if(cycles <= 0){
        printf("No fundamental cycles.");
        return;
    }

    int **circuit = (int **)malloc(cycles * sizeof(int *)); //Define Y axis
    for(int i = 0; i < cycles; i++)
        circuit[i] = (int *)malloc(edgeCount * sizeof(int)); //Define X axis

    for(int i = 0; i < cycles; i++)
        for(int j = 0; j < edgeCount; j++)
            circuit[i][j] = 0;

    // Circuits
    int cycleIndex = 0;
    int edgeIndex;
    int edgeList = getEdgeList(g);

    
    for(int e = 0; e < edgeCount && cycleIndex < cycles; e++){
        circuit[cycleIndex][e] = 1;
        cycleIndex++;
    }
    //TODO
}

void printCutSetMatrix(Graph *g){
    printf("\n=====CutSet Matrix=====\n");
    int edgeCount = countEdges(g);
    if(edgeCount == 0) {
        printf("No hay aristas en el grafo.\n");
        return;
    }

    int cutsets = g->vertices - 1;
    int cutsetMatrix[cutsets][edgeCount];
    for(int i = 0; i < cutsets; i++)
        for(int j = 0; j < edgeCount; j++)
            cutsetMatrix[i][j] = 0;

    int edgeList = getEdgeList(g);
    for(int c = 0; c < cutsets; c++){
        for(int e; e < edgeCount; e++){
            // TODO
        }
    }
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