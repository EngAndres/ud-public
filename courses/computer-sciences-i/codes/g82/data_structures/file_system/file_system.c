/*
This file has a simple implementation of a file system using an N-ary
tree as the underlying data structure.

It includes basic operations such as creating directories and files,
adding children, computing directory sizes via postorder traversal,
searching nodes by name, and printing the tree structure.

Directories are internal nodes and files are leaves. The program also
provides a menu-driven interface for users to interact with the
file system tree.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_MAX 64

typedef enum { FS_DIR, FS_FILE } NodeType;

/* Tree node */
typedef struct FSNode {
    char           name[NAME_MAX];
    NodeType       type;
    int            size_kb;       /* meaningful for files; 0 for dirs */
    struct FSNode *first_child;   /* first child in linked list        */
    struct FSNode *next_sibling;  /* next sibling in linked list       */
} FSNode;

/* Helpers */
static FSNode *new_node(const char *name, NodeType type, int size_kb) {
    FSNode *n = malloc(sizeof(FSNode));
    if (!n) { perror("malloc"); exit(EXIT_FAILURE); }
    strncpy(n->name, name, NAME_MAX - 1);
    n->name[NAME_MAX - 1] = '\0';
    n->type          = type;
    n->size_kb       = size_kb;
    n->first_child   = NULL;
    n->next_sibling  = NULL;
    return n;
}

FSNode *fs_mkdir(const char *name) { return new_node(name, FS_DIR,  0); }
FSNode *fs_mkfile(const char *name, int kb) { return new_node(name, FS_FILE, kb); }

/* Operations */

/* Add `child` as the last child of `parent` — O(children of parent) */
void fs_add_child(FSNode *parent, FSNode *child) {
    if (!parent->first_child) {
        parent->first_child = child;
        return;
    }
    FSNode *cur = parent->first_child;
    while (cur->next_sibling) cur = cur->next_sibling;
    cur->next_sibling = child;
}

/* Postorder traversal: compute total size of a directory subtree — O(n) */
int fs_total_size(const FSNode *node) {
    if (!node) return 0;
    if (node->type == FS_FILE) return node->size_kb;

    int total = 0;
    const FSNode *child = node->first_child;
    while (child) {
        total += fs_total_size(child);
        child  = child->next_sibling;
    }
    return total;
}

/* Search for a node by name (BFS-style preorder) — O(n) */
FSNode *fs_find(FSNode *node, const char *name) {
    if (!node) return NULL;
    if (strcmp(node->name, name) == 0) return node;
    /* Check children */
    FSNode *child = node->first_child;
    while (child) {
        FSNode *found = fs_find(child, name);
        if (found) return found;
        child = child->next_sibling;
    }
    return NULL;
}

/* Pretty-print the tree with indentation — O(n) */
void fs_print(const FSNode *node, int depth) {
    if (!node) return;
    for (int i = 0; i < depth; i++) printf("    ");
    if (node->type == FS_DIR)
        printf("[DIR]  %s/   (total: %d KB)\n", node->name,
               fs_total_size(node));
    else
        printf("[FILE] %s   (%d KB)\n", node->name, node->size_kb);

    const FSNode *child = node->first_child;
    while (child) {
        fs_print(child, depth + 1);
        child = child->next_sibling;
    }
}

/* Free the entire subtree — O(n) postorder */
void fs_free(FSNode *node) {
    if (!node) return;
    FSNode *child = node->first_child;
    while (child) {
        FSNode *next = child->next_sibling;
        fs_free(child);
        child = next;
    }
    free(node);
}

/* main */
void print_menu(void) {
    printf("\n\n\t\tMENU\n");
    printf("1. Print Tree\n");
    printf("2. Get Directory Size\n");
    printf("3. Search Node\n");
    printf("4. Add File to Directory\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    /* Build initial tree */
    FSNode *root     = fs_mkdir("/");
    FSNode *home     = fs_mkdir("home");
    FSNode *etc      = fs_mkdir("etc");
    FSNode *user     = fs_mkdir("user");
    FSNode *docs     = fs_mkdir("docs");
    FSNode *projects = fs_mkdir("projects");
    FSNode *thesis   = fs_mkfile("thesis.pdf", 420);
    FSNode *passwd   = fs_mkfile("passwd",       4);

    fs_add_child(root,     home);
    fs_add_child(root,     etc);
    fs_add_child(home,     user);
    fs_add_child(user,     docs);
    fs_add_child(user,     projects);
    fs_add_child(projects, thesis);
    fs_add_child(etc,      passwd);

    int     option;
    char    name[NAME_MAX];
    char    fname[NAME_MAX];
    int     size_kb;
    FSNode *node;

    /* suppress unused-variable warnings for pre-built nodes */
    (void)docs; (void)projects; (void)thesis; (void)passwd;

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                fs_print(root, 0);
                break;
            case 2:
                printf("Enter directory name: ");
                scanf("%63s", name);
                node = fs_find(root, name);
                if (node)
                    printf("  Total size of '%s': %d KB\n", name, fs_total_size(node));
                else
                    printf("  '%s' not found.\n", name);
                break;
            case 3:
                printf("Enter node name to search: ");
                scanf("%63s", name);
                node = fs_find(root, name);
                if (node)
                    printf("  Found '%s' (%s)\n", name,
                           node->type == FS_DIR ? "directory" : "file");
                else
                    printf("  '%s' not found.\n", name);
                break;
            case 4:
                printf("Enter parent directory name: ");
                scanf("%63s", name);
                node = fs_find(root, name);
                if (!node || node->type != FS_DIR) {
                    printf("  Directory '%s' not found.\n", name);
                    break;
                }
                printf("Enter new file name: ");
                scanf("%63s", fname);
                printf("Enter file size (KB): ");
                scanf("%d", &size_kb);
                fs_add_child(node, fs_mkfile(fname, size_kb));
                printf("  File '%s' added to '%s'.\n", fname, name);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    fs_free(root);
    return 0;
}
