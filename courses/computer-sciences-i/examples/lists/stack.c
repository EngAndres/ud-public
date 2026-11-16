#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

typedef struct {
    Node *head;
    int num_nodes;
} Stack;

Node *createNode(int value){
    Node *new_node = malloc( sizeof(Node) );
    if(new_node == NULL){
        puts("Problema creando el nodo en la memoria.");
        return;
    }

    new_node->value = value;
    return new_node;
}

void initStack(Stack *stack){
    stack->num_nodes = 0;
    stack->head = NULL;
}

bool isEmpty(Stack *stack){
    return stack->num_nodes == 0;
}

void push(Stack *stack, int value){
    Node *new_node = createNode(value);
    new_node->next = stack->head;
    stack->head = new_node;
    stack->num_nodes += 1;
}

Node *pop(Stack *stack){
    if(isEmpty(stack)){
        puts("No hay elementos en la pila, por ende no se puede eliminar.");
        return;
    } else {
        Node *temp = stack->head;
        stack->head = temp->next;
        stack->num_nodes -= 1;
        return temp; 
    }
}

void peak(Stack *stack){
    printf("El contenido de la cima de la pila es: %d", stack->head->value);
}
