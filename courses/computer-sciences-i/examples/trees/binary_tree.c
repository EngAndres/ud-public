#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Student {
    int code;
    char name[50];
    struct Student *left;
    struct Student *right;
} Student;

typedef struct {
    Student *root;
    int size;
} StudentsTree;

Student *createStudent(int code, char name[]){
    Student *new_student = malloc( sizeof(Student) );

    if(new_student == NULL){
        puts("No se ha podido crear al estudiante en la memoria.");
        return NULL;
    }

    new_student->code = code;
    strcpy(new_student->name, name);
    new_student->left = new_student->right = NULL;

    return new_student;
}


Student *insert(Student *root, int new_student_code, char *new_student_name){
    if(root == NULL){
        return createStudent(new_student_code, new_student_name);
    }

    if(new_student_code < root->code){
        root->left = insert(root->left, new_student_code, new_student_name);
    } else if (new_student_code > root->code) {
        root->right = insert(root->right, new_student_code, new_student_name);
    } else {
        printf("Ya existe un estudiante con el código %d.\n", new_student_code);
        return root;
    }

    return root;
}

Student *search(Student *root, int code_to_search){
    if(root == NULL){
        printf("El valor %d no se encontro en los estudiantes.\n", code_to_search);
        return NULL;
    }

    if(code_to_search == root->code){
        return root;
    }

    if(code_to_search < root->code){
        return search(root->left, code_to_search);
    } else {
        return search(root->right, code_to_search);
    }
}

void clean(Student *root){
    if(root != NULL){
        clean(root->left);
        clean(root->right);
        free(root);
    }
}

void preorder(Student *root) {
    if(root != NULL){
        printf("Código: %d  |  Nombre: %s\n", root->code, root->name);
        preorder(root->left);
        preorder(root->right);
    }
}

void inorder(Student *root) {
    if(root != NULL){
        inorder(root->left);
        printf("Código: %d  |  Nombre: %s\n", root->code, root->name);
        inorder(root->right);
    }
}

void postorder(Student *root) {
    if(root != NULL){
        postorder(root->left);
        postorder(root->right);
        printf("Código: %d  |  Nombre: %s\n", root->code, root->name);
    }
}

int main(void){
    StudentsTree tree = { NULL, 0 };
    int option, code, traversal;
    char name[50];

    do {
        puts("\n===== MENÚ DE ESTUDIANTES =====");
        puts("1. Agregar estudiante");
        puts("2. Buscar estudiante por código");
        puts("3. Mostrar estudiantes (recorrido)");
        puts("0. Salir");
        printf("Seleccione una opción: ");

        if(scanf("%d", &option) != 1)
            break;

        switch(option){
            case 1:
                printf("Código: ");
                if(scanf("%d", &code) != 1) { puts("Código no válido."); break; }
                printf("Nombre: ");
                if(scanf(" %49[^\n]", name) != 1) { puts("Nombre no válido."); break; }
                tree.root = insert(tree.root, code, name);
                break;

            case 2: {
                Student *found;
                printf("Código a buscar: ");
                if(scanf("%d", &code) != 1) { puts("Código no válido."); break; }
                found = search(tree.root, code);
                if(found != NULL)
                    printf("Encontrado -> Código: %d  |  Nombre: %s\n", found->code, found->name);
                break;
            }

            case 3:
                if(tree.root == NULL){
                    puts("No hay estudiantes registrados.");
                    break;
                }
                puts("Tipo de recorrido:");
                puts("1. Preorden");
                puts("2. Inorden");
                puts("3. Postorden");
                printf("Seleccione: ");
                if(scanf("%d", &traversal) != 1) { puts("Recorrido no válido."); break; }

                if(traversal == 1){
                    puts("--- Recorrido Preorden ---");
                    preorder(tree.root);
                } else if(traversal == 2){
                    puts("--- Recorrido Inorden ---");
                    inorder(tree.root);
                } else if(traversal == 3){
                    puts("--- Recorrido Postorden ---");
                    postorder(tree.root);
                } else {
                    puts("Recorrido no válido.");
                }
                break;

            case 0:
                break;

            default:
                puts("Opción no válida.");
        }
    } while(option != 0);

    clean(tree.root);
    tree.root = NULL;
    puts("Programa finalizado.");
    return 0;
}
