/*
This file has a simple implementation of a round-robin CPU scheduler
using a circular singly-linked list as the underlying data structure.

It includes basic operations such as adding a process, running one
time quantum, printing the queue status, and freeing all processes.

The scheduler cycles through all processes giving each a fixed time
slice. The circular structure handles wrap-around naturally without
any restart logic. The program also provides a menu-driven interface
for users to interact with the scheduler.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_MAX 32

/* Node definition */
typedef struct Process {
    int pid;
    char name[NAME_MAX];
    int burst;      /* total CPU time needed      */
    int remaining;  /* CPU time still to execute  */
    struct Process *next;
} Process;

/* Scheduler handle */
typedef struct {
    Process *tail;         /* tail->next == head */
    int time_quantum;
    int count;
} RRScheduler;

/* Helpers */
static Process *new_process(int pid, const char *name, int burst) {
    Process *p = malloc(sizeof(Process));
    if (!p) { 
        perror("Memory allocation failed."); 
        exit(EXIT_FAILURE); 
    }
    p->pid = pid;
    p->burst = burst;
    p->remaining = burst;
    strncpy(p->name, name, NAME_MAX - 1);
    p->name[NAME_MAX - 1] = '\0';
    p->next = NULL;
    return p;
}

void rr_init(RRScheduler *s, int quantum) {
    s->tail = NULL;
    s->time_quantum = quantum;
    s->count = 0;
}

/* Operations */

/* Add a process to the circular list — O(1) */
void add_process(RRScheduler *s, int pid, const char *name, int burst) {
    Process *p = new_process(pid, name, burst);
    if (!s->tail) {
        p->next = p;  /* point to itself */
        s->tail = p;
    } else {
        p->next = s->tail->next;  /* new->next = head */
        s->tail->next = p;  /* old tail -> new  */
        s->tail = p;  /* new is now tail  */
    }
    s->count++;
    printf("  Added: PID %d (%s) burst=%d\n", pid, name, burst);
}

/* Remove a finished process (remaining == 0) pointed to by prev->next — O(1) */
static void remove_node(RRScheduler *s, Process *prev) {
    Process *target = prev->next;
    if (s->count == 1) {  /* last process */
        s->tail = NULL;
    } else {
        prev->next = target->next;
        if (target == s->tail)
            s->tail = prev;
    }
    printf("  Finished: PID %d (%s)\n", target->pid, target->name);
    free(target);
    s->count--;
}

/* Give one time quantum to the current (head) process, then advance — O(1) */
void run_quantum(RRScheduler *s) {
    if (!s->tail) { 
        puts("  run_quantum: no processes"); 
        return; 
    }

    Process *head = s->tail->next;
    int slice = (head->remaining < s->time_quantum)
                ? head->remaining
                : s->time_quantum;
    head->remaining -= slice;
    printf("  Running : PID %d (%s)  slice=%d  remaining=%d\n",
           head->pid, head->name, slice, head->remaining);

    if (head->remaining == 0)
        remove_node(s, s->tail);   /* tail->next is head */
    else
        s->tail = head;            /* advance: old head becomes new tail */
}

/* Print all waiting processes in circular order — O(n) */
void print_status(const RRScheduler *s) {
    if (!s->tail) { 
        puts("  (no processes)"); 
        return; 
    }
    
    printf("  Queue   : ");
    Process *cur = s->tail->next;  /* start from head */
    do {
        printf("PID%d(%s,rem=%d) → ", cur->pid, cur->name, cur->remaining);
        cur = cur->next;
    } while (cur != s->tail->next);
    puts("(wrap)");
}

/* Free all remaining processes */
void rr_free(RRScheduler *s) {
    if (!s->tail) 
        return;
    
    Process *head = s->tail->next;
    s->tail->next = NULL;          /* break the cycle */
    Process *cur  = head;
    while (cur) {
        Process *tmp = cur->next;
        free(cur);
        cur = tmp;
    }
    s->tail  = NULL;
    s->count = 0;
}

/* main */
void print_menu(void) {
    printf("\n\n\t\tMENU\n");
    printf("1. Add Process\n");
    printf("2. Run One Quantum\n");
    printf("3. Print Status\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    RRScheduler s;
    rr_init(&s, 3);
    int option;
    int pid, burst;
    char name[NAME_MAX];

    do {
        print_menu();
        if (scanf("%d", &option) != 1) {
            int c;
            while ((c = getchar()) != '\n' && c != EOF)
                ;
            if (c == EOF) break;
            option = -1;  /* fall through to default */
        }

        switch (option) {
            case 1:
                printf("Enter PID: ");
                scanf("%d", &pid);
                printf("Enter name: ");
                scanf("%31s", name);
                printf("Enter burst time: ");
                scanf("%d", &burst);
                add_process(&s, pid, name, burst);
                break;
            case 2:
                run_quantum(&s);
                break;
            case 3:
                print_status(&s);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    rr_free(&s);
    return 0;
}
