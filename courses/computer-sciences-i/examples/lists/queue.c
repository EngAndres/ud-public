#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

typedef struct  {
    int num_nodes;
    Node *head;
    Node *tail;
} Queue;

Node *newNode(int value){
    Node *new_node = malloc( sizeof(Node) );
    if(new_node == NULL){
        puts("Problemas creando el nodo en la memoria.");
        return;
    }

    new_node->value = value;
    return new_node;
}

void initQueue(Queue *queue){
    queue->num_nodes = 0;
    queue->head = NULL;
    queue->tail = NULL;
}

bool isEmpty(Queue *queue){
    return queue->num_nodes == 0;
}

void enqueue(Queue *queue, int value){
    Node *new_node = newNode(value);
    new_node->next = NULL;
    Node *last = queue->tail;
    last->next = new_node;
    queue->tail = new_node;
    queue->num_nodes += 1;
}

Node *dequeue(Queue *queue){
    if(isEmpty(queue)){
        puts("No se puede eliminar un elemento de la fila porque está vacía.");
        return;
    } else {
        Node *temp = queue->head;
        queue->head = temp->next;
        queue->num_nodes -= 1;
        return temp;
    }
}

void front(Queue *queue){
    if(isEmpty(queue)){
        puts("No se puede ver el primer elemento de la fila porque está vacía.");
        return;
    } else {
        printf("El valor en el primer elemento de la fila es: %d", queue->head->value);
    }
}