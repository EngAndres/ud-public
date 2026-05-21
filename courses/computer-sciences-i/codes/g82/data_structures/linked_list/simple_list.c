#include <stdio.h>
#include <stdlib.h>

typedef struct Student {
    int code;
    double grade;
    struct Student *next; // Pointer, default null
} Student;

typedef struct {
    Student *head;
    int size;
} LinkedList;

static Student *new_student(int new_code, double new_grade){
    Student *s = malloc(sizeof(Student));
    if(!s){
        perror("Malloc fails.");
        exit(EXIT_FAILURE);
    }
    s->code = new_code;
    s->grade = new_grade;
    return s;
}

void init_list(LinkedList *list) {
    list->head = NULL;
    list->size = 0;
}

/* INSERT */
void insert_begin(LinkedList *list, int code, double grade){
    Student *student_begin = new_student(code, grade);
    student_begin->next = list->head;
    list->head = student_begin;
    list->size++;
}

void insert_end(LinkedList *list, int code, double grade){
    Student *student_end = new_student(code, grade);
    if(!list->head){
        list-> head = student_end;
    } else {
        Student *last = list-> head;
        while(last->next)
            last = last->next;
        last->next = student_end;
    }
    list->size++;
}

void insert_position(LinkedList *list, int position, int code, double grade){
    if(position < 0 || position >= list->size){
        fprintf(stderr, "insert_position: position %d out of range (size=%d)\n", 
            position, list->size);
        return;
    }
    Student *current_node = list->head;
    for(int i = 0; i < position; i++)
        current_node = current_node->next;

    Student *student_pos = new_student(code, grade);
    student_pos->next = current_node->next;
    current_node->next = student_pos;
    list->size++;
}

// Delete

void delete_begin(LinkedList *list){
    if(!list->head){
        puts("List is empty. Cannot apply deletion.");
        return;
    }

    Student *temp = list->head;
    list->head = temp->next;
    free(temp);
    list->size--;
}

void delete_end(LinkedList *list){
    if(!list->head){
        puts("Cannot delete, list empty");
        return;
    }
    if(!list->head->next) { // First is the last, list of size 1
        free(list->head);
        list->head = NULL;
        list->size--;
        return;
    }
    Student *prev = list->head;
    while(prev->next->next)
        prev = prev->next;
    free(prev->next);
    prev->next = NULL;
    list->size--;
}

void delete_middle(LinkedList *list, int position){
    if(position < 0 || position >= list->size){
        fprintf(stderr, "Index out of range. Delete unsuccessful: %d index and %d size.\n",
        position, list->size);
        return;
    }
    if(position == 0){
        delete_begin(list);
        return;
    }
    Student *prev = list->head;
    for(int i = 0; i < position - 1; i++)
        prev = prev->next;

    Student *temp = prev->next;
    prev->next = temp->next;
    free(temp);
    list->size--;
}

// Additionals
int linear_search_by_code(LinkedList *list, int code_){
    Student *s = list->head;
    int index = 0;
    while(s){
        if(s->code == code_){
            return index;
        }
        s = s->next;
        index++;
    }
    return -1;
}

void print_list(LinkedList *list){
    if(!list->head){
        puts("Empty List.");
        return;
    }
    Student *s = list->head;
    printf(" HEAD\n");
    while(s){
        printf("Code: %d\tGrade:%.1f \n", s->code, s->grade);
        s = s->next;
    }
    printf(" TAIL -> NULL, size=%d\n", list->size);
}

void free_memory(LinkedList *list){
    Student *temp = list->head;
    while(temp){
        Student *next = temp->next;
        free(temp);
        temp = next;
    }
    list->head = NULL;
}

int main(void){

    LinkedList *list;
    init_list(&list);

    insert_begin(&list, 1, 3.6);
    insert_begin(&list, 2, 4.2);
    insert_end(&list, 3, 3.2);
    insert_end(&list, 4, 3.2);
    insert_position(&list, 2, 5, 3.0);

    print_list(&list);

    delete_begin(&list);
    delete_end(&list);
    delete_middle(&list, 1);

    print_list(&list);

    for(int code = 1; code <= 5; code++){
        if(linear_search_by_code(&list, code) == -1){
            printf("Number %d not found\n", code);
        } else {
            printf("Number %d exists\n", code);
        }
    }

    return 0;
}