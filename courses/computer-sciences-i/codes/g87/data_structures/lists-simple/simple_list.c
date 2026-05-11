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

void insert_middle(LinkedList *list, int position, int new_code, double new_avg_grade){
    if(position < 0 || position >= list->size){
        fprintf(stderr, "Index out of range. Index %d is out size %d.\n",
                        position, list->size);
        return;
    }
    
    Student *current = list->head;
    for(int i = 0; i < position - 1; i++)
        current = current->next;

    Student *s = new_student(new_code, new_avg_grade);
    s->next = current->next;
    current->next = s;
    list->size++;
}

// Deletions

void delete_begin(LinkedList *list){
    if(!list->head){ //Empty list
        puts("delete_begin: cannot delete in an empty list.");
        return;
    }

    Student *temp = list->head;
    list->head = temp->next;
    free(temp);
    list->size--;
}

void delete_end(LinkedList *list){
    if(!list->head){ //Empty list
        puts("delete_end: cannot delete in an empty list.");
        return;
    }
    if(!list->head->next){ //Only 1 element
        free(list->head);
        list->head = NULL;
        list->size--;
        return;
    }
    //2 elements at least
    Student *current = list->head;
    while(current->next->next)
        current = current->next;

    free(current->next);
    current->next = NULL;
    list->size--;
}

void delete_middle(LinkedList *list, int position){
    if(position < 0 || position >= list->size){
        fprintf(stderr, "Index out of range. Index %d is out size %d.\n",
                        position, list->size);
        return;
    }
    if(position == 0){
        delete_begin(list);
        return;
    }

    Student *prev = list->head;
    for(int i = 0; i < position-1; i++)
        prev = prev->next;

    Student *temp = prev->next;
    prev->next = temp->next;
    free(temp);
    list->size--;
}

// Utilities

int lineal_search(const LinkedList *list, int code){
    Student *current = list->head;
    int index = 0;
    while(current){
        if(current->code == code)
            return index;
        
        current = current->next;
        index++;
    }
    return -1;
}

void print_list(const LinkedList *list){
    if(!list->head){
        puts("List is empty");
        return;
    }

    printf("\tHEAD\n");
    Student *current = list->head;
    while(current){
        printf("Code: %d -> Grade: %.1f\n", current->code, current->avg_grade);
        current = current->next;
    }
    printf("\tTAIL.\n");
    printf("Size: %d\n\n", list->size);
}

void list_free(LinkedList *list){
    Student *current = list->head;
    while(current){
        Student *temp = current->next;
        free(current);
        current = temp;
    }
    list->head = NULL;
    list->size = 0;
}



int main(void){
    LinkedList list;
    list_init(&list);

    insert_begin(&list, 1, 4.5);
    insert_begin(&list, 2, 3.8);
    insert_end(&list, 3, 2.8);
    insert_end(&list, 4, 3.8);
    insert_middle(&list, 2, 5, 4.0);
    print_list(&list);

    delete_begin(&list);
    delete_end(&list);
    delete_middle(&list, 1);
    print_list(&list);

    for(int i = 1; i <= 5; i++){
        int index = lineal_search(&list, i);
        if(index == -1){
            printf("Code %d does not exist.\n", i);
        } else {
            printf("Code %d is at %d index.\n", i, index);
        }
    }

    list_free(&list);
    return 0;
}


