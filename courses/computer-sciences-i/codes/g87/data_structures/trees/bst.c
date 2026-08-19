/* ============================================================
 * Binary Search Tree — insert, delete, search + traversals
 * Traversals: inorder, preorder, postorder, level-order
 * ============================================================ */
#include <stdio.h>
#include <stdlib.h>

/* ── Node ──────────────────────────────────────────────────── */
typedef struct Node {
    int data;
    struct Node *left, *right;
} Node;

static Node *newNode(int data) {
    Node *n = malloc(sizeof(Node));
    n->data  = data;
    n->left  = n->right = NULL;
    return n;
}

/* ── Core operations ───────────────────────────────────────── */
Node *bst_insert(Node *root, int data) {
    if (!root) // subtree root
        return newNode(data);
    
    if(data < root->data) 
        root->left  = bst_insert(root->left,  data);
    else if (data > root->data) 
        root->right = bst_insert(root->right, data);
    return root;   /* duplicate: ignore */
}

static Node *minNode(Node *n) {
    while (n->left)
        n = n->left;
    return n;
}

Node *bst_delete(Node *root, int data) {
    if (!root) 
        return NULL;

    if(data < root->data) 
        root->left  = bst_delete(root->left,  data);
    else if (data > root->data) 
        root->right = bst_delete(root->right, data);
    else {
        /* node with one or no child */
        if (!root->left)  { 
            Node *t = root->right; 
            free(root); 
            return t; }
        if (!root->right) { 
            Node *t = root->left;  
            free(root); 
            return t; 
        }
        /* node with two children: replace with in-order successor */
        Node *succ   = minNode(root->right);
        root->data   = succ->data;
        root->right  = bst_delete(root->right, succ->data);
    }
    return root;
}

Node *bst_search(Node *root, int data) {
    if (!root || root->data == data) 
        return root;
    return data < root->data ? bst_search(root->left, data)
                             : bst_search(root->right, data);
}

/* ── Traversals ────────────────────────────────────────────── */
void inorder(Node *root) {
    if (!root) 
        return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

void preorder(Node *root) {
    if (!root) 
        return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

void postorder(Node *root) {
    if (!root) 
        return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}

void levelorder(Node *root) {
    if (!root) 
        return;
    Node *queue[1024];
    int front = 0, rear = 0;
    queue[rear++] = root;
    while (front < rear) {
        Node *cur = queue[front++];
        printf("%d ", cur->data);
        if (cur->left)  queue[rear++] = cur->left;
        if (cur->right) queue[rear++] = cur->right;
    }
}

/* ── Utility ───────────────────────────────────────────────── */
int bst_height(Node *root) {
    if (!root) 
        return 0;
    int l = bst_height(root->left), r = bst_height(root->right);
    return 1 + (l > r ? l : r);
}

void freeTree(Node *root) {
    if (!root) 
        return;
    freeTree(root->left);
    freeTree(root->right);
    free(root);
}

/* ── Demo ──────────────────────────────────────────────────── */
int main(void) {
    Node *root = NULL;
    int keys[] = {50, 30, 70, 20, 40, 60, 80};
    int n = (int)(sizeof(keys) / sizeof(keys[0]));

    printf("=== Binary Search Tree ===\n\n");

    for (int i = 0; i < n; i++)
        root = bst_insert(root, keys[i]);

    printf("Inorder    (sorted)  : "); inorder(root);    printf("\n");
    printf("Preorder   (root 1st): "); preorder(root);   printf("\n");
    printf("Postorder  (root lst): "); postorder(root);  printf("\n");
    printf("Level-order (BFS)    : "); levelorder(root); printf("\n");
    printf("Height               : %d\n", bst_height(root));

    printf("\nSearch 40  -> %s\n", bst_search(root, 40) ? "found" : "not found");
    printf("Search 55  -> %s\n",  bst_search(root, 55) ? "found" : "not found");

    printf("\nDelete 30 (node with two children):\n");
    root = bst_delete(root, 30);
    printf("Inorder after delete : "); inorder(root); printf("\n");

    printf("\nDelete 70 (node with two children):\n");
    root = bst_delete(root, 70);
    printf("Inorder after delete : "); inorder(root); printf("\n");

    freeTree(root);
    return 0;
}
