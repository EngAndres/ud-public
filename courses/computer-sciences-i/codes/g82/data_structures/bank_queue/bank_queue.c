/*
This file has a simple implementation of a bank queue system using a
FIFO queue as the underlying data structure.

It includes basic operations such as issuing tickets to customers,
calling the next customer, checking the wait count, and printing
the current queue status.

The queue guarantees fair service: the first customer to arrive is
the first to be served. The program also provides a menu-driven
interface for users to interact with the bank queue.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_MAX 64

/* Queue node */
typedef struct QNode {
    int            ticket;
    char           name[NAME_MAX];
    struct QNode  *next;
} QNode;

/* Queue */
typedef struct {
    QNode *front; //read
    QNode *rear; //add
    int    size;
} Queue;

/* Queue helpers */
void queue_init(Queue *q) {
    q->front = q->rear = NULL;
    q->size  = 0;
}

int queue_empty(const Queue *q) { 
    return q->front == NULL; 
}

void enqueue(Queue *q, int ticket, const char *name) {
    QNode *n = malloc(sizeof(QNode));
    if (!n) { 
        perror("malloc"); 
        exit(EXIT_FAILURE); 
    }
    n->ticket = ticket;
    strncpy(n->name, name, NAME_MAX - 1);
    n->name[NAME_MAX - 1] = '\0';
    n->next = NULL;
    if (q->rear)
        q->rear->next = n;
    else
        q->front = n;
    q->rear = n;
    q->size++;
}

/* Returns the dequeued node (caller frees it) */
static QNode *dequeue_node(Queue *q) {
    if (queue_empty(q))
        return NULL;
    QNode *tmp = q->front;
    q->front   = tmp->next;
    if (!q->front) 
        q->rear = NULL;
    q->size--;
    return tmp;
}

/* BankQueue */
typedef struct {
    Queue queue;
    int   next_ticket;
} BankQueue;

void bq_init(BankQueue *b) {
    queue_init(&b->queue);
    b->next_ticket = 1;
}

/* Assign the next ticket number and enqueue the customer — O(1) */
int take_ticket(BankQueue *b, const char *name) {
    int ticket = b->next_ticket++;
    enqueue(&b->queue, ticket, name);
    printf("  Ticket %-3d issued to: %s\n", ticket, name);
    return ticket;
}

/* Serve the next customer in line — O(1) */
void call_next(BankQueue *b) {
    QNode *n = dequeue_node(&b->queue);
    if (!n) {
        puts("  call_next: no customers waiting");
        return;
    }
    printf("  Serving ticket %-3d: %s\n", n->ticket, n->name);
    free(n);
}

/* How many customers are still waiting — O(1) */
int get_wait_count(const BankQueue *b) {
    return b->queue.size;
}

/* Print all waiting customers */
void print_status(const BankQueue *b) {
    if (queue_empty(&b->queue)) {
        puts("  Status  : (no customers waiting)");
        return;
    }
    printf("  Waiting (%d): ", b->queue.size);
    const QNode *cur = b->queue.front;
    while (cur) {
        printf("[#%d %s] ", cur->ticket, cur->name);
        cur = cur->next;
    }
    puts("");
}

/* Free remaining nodes */
void bq_free(BankQueue *b) {
    QNode *n;
    while ((n = dequeue_node(&b->queue)) != NULL)
        free(n);
}

/* main */
void print_menu(void) {
    printf("\n\n\t\tMENU\n");
    printf("1. Take Ticket\n");
    printf("2. Call Next\n");
    printf("3. Get Wait Count\n");
    printf("4. Print Status\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    BankQueue b;
    bq_init(&b);
    int option;
    char name[NAME_MAX];

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Enter customer name: ");
                scanf("%63s", name);
                take_ticket(&b, name);
                break;
            case 2:
                call_next(&b);
                break;
            case 3:
                printf("  Customers waiting: %d\n", get_wait_count(&b));
                break;
            case 4:
                print_status(&b);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    bq_free(&b);
    return 0;
}
