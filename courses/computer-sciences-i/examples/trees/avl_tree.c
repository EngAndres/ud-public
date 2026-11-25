#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct Student {
    int code;
    char name[50];
    int internal_height;
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
    new_student->internal_height = 1;
    strcpy(new_student->name, name);
    new_student->left = new_student->right = NULL;

    return new_student;
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

// AVL Changes
int height(Student *student){
    if(student == NULL){
        return 0;
    }
    return student->internal_height;
}

int balance_factor(Student *student){
    if(student == NULL){
        return 0;
    }
    return abs(altura(student->left) - altura(student->right));
}

int max(int num_1, int num_2){
    return num_1 > num_2? num_1 : num_2;
}

Student *singleRightRotation(Student *z){
    Student *y = z->left;
    Student *temp = y->right;

    y->right = z;
    z->left = temp;

    z->internal_height = 1 + max( height(z->left), height(z->right) );
    y->internal_height = 1 + max( height(y->left), height(y->right) );

    return y;
}

Student *singleLeftRotation(Student *z){
    Student *y = z->right;
    Student *temp = y->left;

    y->left = z;
    z->right = temp;

    z->internal_height = 1 + max( height(z->left), height(z->right) );
    y->internal_height = 1 + max( height(y->left), height(y->right) );

    return y;
}

// Inserta recursivamente, actualiza alturas y rebalancea con rotaciones
Student *insertStudentAVL(Student *root, int code, char name[], int *inserted){
    if(root == NULL){
        Student *new_student = createStudent(code, name);
        if(new_student != NULL){
            *inserted = 1;
        }
        return new_student;
    }

    if(code < root->code){
        root->left = insertStudentAVL(root->left, code, name, inserted);
    } else if(code > root->code){
        root->right = insertStudentAVL(root->right, code, name, inserted);
    } else {
        printf("El codigo %d ya existe, no se inserta.\n", code);
        return root;
    }

    // Actualizar la altura del nodo
    root->internal_height = 1 + max( height(root->left), height(root->right) );

    // Factor de balance con signo: altura(izquierda) - altura(derecha)
    int balance = height(root->left) - height(root->right);

    // Caso izquierda-izquierda
    if(balance > 1 && code < root->left->code){
        return singleRightRotation(root);
    }

    // Caso izquierda-derecha
    if(balance > 1 && code > root->left->code){
        root->left = singleLeftRotation(root->left);
        return singleRightRotation(root);
    }

    // Caso derecha-derecha
    if(balance < -1 && code > root->right->code){
        return singleLeftRotation(root);
    }

    // Caso derecha-izquierda
    if(balance < -1 && code < root->right->code){
        root->right = singleRightRotation(root->right);
        return singleLeftRotation(root);
    }

    return root;
}

// Inserta un estudiante en el arbol. Retorna 1 si se inserto, 0 si no.
int insertStudent(StudentsTree *tree, int code, char name[]){
    int inserted = 0;

    tree->root = insertStudentAVL(tree->root, code, name, &inserted);

    if(inserted){
        tree->size++;
        return 1;
    }
    return 0;
}

int main(void){
    StudentsTree tree = { NULL, 0 };
    int option = -1;
    int code;
    char name[50];

    do {
        printf("\n1. Insertar estudiante\n");
        printf("2. Mostrar estudiantes (inorder)\n");
        printf("3. Mostrar altura de la raiz\n");
        printf("0. Salir\n");
        printf("Opcion: ");

        if(scanf("%d", &option) != 1){
            break;
        }
        getchar();

        switch(option){
            case 1:
                printf("Codigo: ");
                scanf("%d", &code);
                getchar();
                printf("Nombre: ");
                fgets(name, sizeof(name), stdin);
                name[strcspn(name, "\n")] = '\0';

                if(insertStudent(&tree, code, name)){
                    puts("Estudiante insertado.");
                }
                break;
            case 2:
                inorder(tree.root);
                printf("Total de estudiantes: %d\n", tree.size);
                break;
            case 3:
                printf("Altura de la raiz: %d\n", height(tree.root));
                break;
            case 0:
                puts("Saliendo...");
                break;
            default:
                puts("Opcion invalida.");
        }
    } while(option != 0);

    clean(tree.root);
    return 0;
}