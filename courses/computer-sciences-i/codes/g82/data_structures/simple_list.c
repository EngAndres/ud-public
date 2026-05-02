#include <stdio.h>
#include <stdlib.h>

typedef struct Student {
    int code;
    double grade;
    struct Student *next; // Pointer
} Student;