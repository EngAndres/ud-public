/*
This file has a simple implementation of an undo/redo system using
two stacks as the underlying data structure.

It includes basic operations such as recording an edit action, undoing
the last action, redoing the last undone action, and printing both
stack states.

Recording a new action always clears the redo stack. The program also
provides a menu-driven interface for users to interact with the
undo/redo manager.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DESC_MAX 128

/* Edit action */
typedef struct {
    char description[DESC_MAX];
} EditAction;

/* Stack node */
typedef struct SNode {
    EditAction    action;
    struct SNode *next;
} SNode;

/* Stack */
typedef struct {
    SNode *top;
    int    size;
} Stack;

/* Stack helpers */
void stack_init(Stack *s) {
    s->top  = NULL;
    s->size = 0;
}

int stack_empty(const Stack *s) { 
    return s->top == NULL; 
}

void stack_push(Stack *s, EditAction a) {
    SNode *n = malloc(sizeof(SNode));
    if (!n) { 
        perror("malloc"); 
        exit(EXIT_FAILURE); 
    }
    n->action = a;
    n->next   = s->top;
    s->top    = n;
    s->size++;
}

EditAction stack_pop(Stack *s) {
    if (stack_empty(s)) {
        fprintf(stderr, "stack_pop: stack is empty\n");
        exit(EXIT_FAILURE);
    }
    SNode *tmp = s->top;
    EditAction a = tmp->action;
    s->top  = tmp->next;
    free(tmp);
    s->size--;
    return a; 
}

void stack_clear(Stack *s) {
    while (!stack_empty(s)) 
        stack_pop(s);
}

void stack_print(const Stack *s, const char *label) {
    printf("  %-14s: ", label);
    if (stack_empty(s)) { puts("(empty)"); return; }
    SNode *cur = s->top;
    while (cur) {
        printf("[%s] ", cur->action.description);
        cur = cur->next;
    }
    puts("(bottom)");
}

/* UndoManager */
typedef struct {
    Stack undo_stack;
    Stack redo_stack;
} UndoManager;

void um_init(UndoManager *m) {
    stack_init(&m->undo_stack);
    stack_init(&m->redo_stack);
}

/* Record a new action: push to undo, wipe redo — O(1) push + O(k) clear */
void record(UndoManager *m, const char *desc) {
    EditAction a;
    strncpy(a.description, desc, DESC_MAX - 1);
    a.description[DESC_MAX - 1] = '\0';
    stack_push(&m->undo_stack, a);
    stack_clear(&m->redo_stack);
    printf("  Recorded: %s\n", desc);
}

/* Undo last action — O(1) */
void undo(UndoManager *m) {
    if (stack_empty(&m->undo_stack)) {
        puts("  undo: nothing to undo");
        return;
    }
    EditAction a = stack_pop(&m->undo_stack);
    stack_push(&m->redo_stack, a);
    printf("  Undone  : %s\n", a.description);
}

/* Redo last undone action — O(1) */
void redo(UndoManager *m) {
    if (stack_empty(&m->redo_stack)) {
        puts("  redo: nothing to redo");
        return;
    }   
    EditAction a = stack_pop(&m->redo_stack);
    stack_push(&m->undo_stack, a);
    printf("  Redone  : %s\n", a.description);
}

/* Free both stacks */
void um_free(UndoManager *m) {
    stack_clear(&m->undo_stack);
    stack_clear(&m->redo_stack);
}

/* Print both stacks (top is most recent) */
void um_print(const UndoManager *m) {
    stack_print(&m->undo_stack, "undo_stack");
    stack_print(&m->redo_stack, "redo_stack");
}

/* main */
void print_menu(void) {
    printf("\n\n\t\tMENU\n");
    printf("1. Record Action\n");
    printf("2. Undo\n");
    printf("3. Redo\n");
    printf("4. Print Stacks\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    UndoManager m;
    um_init(&m);
    int option;
    char desc[DESC_MAX];

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Enter action description: ");
                scanf(" %127[^\n]", desc);
                record(&m, desc);
                break;
            case 2:
                undo(&m);
                break;
            case 3:
                redo(&m);
                break;
            case 4:
                um_print(&m);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    um_free(&m);
    return 0;
}
