#include <stdio.h>
#include <stdlib.h>

typedef struct Student {
    int code;
    double avg_grade;
    struct Student *next; //Pointer
} Student;

typedef struct {
    Student *head;
    int size;
} LinkedList;

// Basic Functions
static Student *new_student(int new_code, double new_avg_grade) {
    Student *s = malloc(sizeof(Student));
    if(!s){
        perror("Malloc Failed.");
        exit(EXIT_FAILURE);
    }
    s->code = new_code;
    s->avg_grade = new_avg_grade;
    return s;
}

void list_init(LinkedList *list) {
    list->head = NULL;
    list->size = 0;
}

/// Insertions

void insert_begin(LinkedList *list, int new_code, double new_avg_grade){
    Student *s = new_student(new_code, new_avg_grade);
    s->next = list->head;
    list->head = s;
    list->size++;
}

void insert_end(LinkedList *list, int new_code, double new_avg_grade){
    Student *s = new_student(new_code, new_avg_grade);
    if(!list->head){
        list->head = s;
    } else {
        Student *current = list->head;
        while(current->next)
            current = current->next;
        current->next = s;
    }
    list->size++;
}

void insert_middle(LinkedList *list, int new_code, double new_avg_grade){

}




