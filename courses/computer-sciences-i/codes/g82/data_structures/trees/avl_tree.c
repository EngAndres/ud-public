/* ============================================================
 * AVL Tree — self-balancing BST
 * Operations: insert, delete, search + inorder / preorder
 * Each node stores its height; rotations keep |bf| <= 1.
 * ============================================================ */
#include <stdio.h>
#include <stdlib.h>

/* ── Node ──────────────────────────────────────────────────── */
typedef struct AVLNode {
    int data;
    int height;
    struct AVLNode *left, *right;
} AVLNode;

static int avlHeight(AVLNode *n)  { 
    return n ? n->height : 0; 
}
static int imax(int a, int b) { 
    return a > b ? a : b; 
}

static int balanceFactor(AVLNode *n)  { 
    return avlHeight(n->left) - avlHeight(n->right); 
}

static void updateHeight(AVLNode *n) {
    if (n)
        n->height = 1 + imax(avlHeight(n->left), avlHeight(n->right));
}

static AVLNode *newAVLNode(int data) {
    AVLNode *n = malloc(sizeof(AVLNode));
    n->data   = data;
    n->height = 1;
    n->left   = n->right = NULL;
    return n;
}

/* ── Rotations ─────────────────────────────────────────────── */
/*
 *     y                x
 *    / \     RR       / \
 *   x   T3  ---->   T1   y
 *  / \                  / \
 * T1 T2                T2  T3
 */
static AVLNode *rotateRight(AVLNode *y) {
    AVLNode *x  = y->left;
    AVLNode *T2 = x->right;
    x->right = y;
    y->left  = T2;
    updateHeight(y);
    updateHeight(x);
    return x;           /* new subtree root */
}

/*
 *   x                   y
 *  / \     RL          / \
 * T1  y   ---->       x   T3
 *    / \             / \
 *   T2 T3           T1 T2
 */
static AVLNode *rotateLeft(AVLNode *x) {
    AVLNode *y  = x->right;
    AVLNode *T2 = y->left;
    y->left  = x;
    x->right = T2;
    updateHeight(x);
    updateHeight(y);
    return y;           /* new subtree root */
}

/* ── Rebalance after any structural change ─────────────────── */
static AVLNode *rebalance(AVLNode *n) {
    updateHeight(n);
    int bf = balanceFactor(n);

    /* Left-Left  */
    if (bf >  1 && balanceFactor(n->left) >= 0)
        return rotateRight(n);

    /* Left-Right */
    if (bf >  1 && balanceFactor(n->left) < 0) {
        n->left = rotateLeft(n->left);
        return rotateRight(n);
    }

    /* Right-Right */
    if (bf < -1 && balanceFactor(n->right) <= 0)
        return rotateLeft(n);

    /* Right-Left  */
    if (bf < -1 && balanceFactor(n->right) > 0) {
        n->right = rotateRight(n->right);
        return rotateLeft(n);
    }

    return n;   /* already balanced */
}

/* ── Core operations ───────────────────────────────────────── */
AVLNode *avl_insert(AVLNode *root, int data) {
    if (!root) return newAVLNode(data);
    if      (data < root->data) root->left  = avl_insert(root->left,  data);
    else if (data > root->data) root->right = avl_insert(root->right, data);
    else return root;   /* duplicate: ignore */
    return rebalance(root);
}

static AVLNode *avlMin(AVLNode *n) {
    while (n->left) n = n->left;
    return n;
}

AVLNode *avl_delete(AVLNode *root, int data) {
    if (!root) return NULL;
    if      (data < root->data) root->left  = avl_delete(root->left,  data);
    else if (data > root->data) root->right = avl_delete(root->right, data);
    else {
        if (!root->left || !root->right) {
            AVLNode *child = root->left ? root->left : root->right;
            free(root);
            return child;
        }
        /* two children: swap with in-order successor, then delete it */
        AVLNode *succ = avlMin(root->right);
        root->data    = succ->data;
        root->right   = avl_delete(root->right, succ->data);
    }
    return rebalance(root);
}

AVLNode *avl_search(AVLNode *root, int data) {
    if (!root || root->data == data) return root;
    return data < root->data ? avl_search(root->left, data)
                             : avl_search(root->right, data);
}

/* ── Traversals ────────────────────────────────────────────── */
void avl_inorder(AVLNode *root) {
    if (!root) return;
    avl_inorder(root->left);
    printf("%d(h=%d,bf=%+d) ", root->data, root->height, balanceFactor(root));
    avl_inorder(root->right);
}

void avl_preorder(AVLNode *root) {
    if (!root) return;
    printf("%d(h=%d,bf=%+d) ", root->data, root->height, balanceFactor(root));
    avl_preorder(root->left);
    avl_preorder(root->right);
}

void freeAVL(AVLNode *root) {
    if (!root) return;
    freeAVL(root->left);
    freeAVL(root->right);
    free(root);
}

/* ── Demo ──────────────────────────────────────────────────── */
int main(void) {
    AVLNode *root = NULL;

    /* Inserting in sorted order would create a skewed BST but
       an AVL tree will keep rebalancing itself automatically.  */
    int keys[] = {10, 20, 30, 40, 50, 25};
    int n = (int)(sizeof(keys) / sizeof(keys[0]));

    printf("=== AVL Tree ===\n\n");
    printf("%-10s %-8s %-6s %s\n", "Operation", "Root", "Height", "BF@root");
    printf("--------------------------------------------\n");

    for (int i = 0; i < n; i++) {
        root = avl_insert(root, keys[i]);
        printf("insert %-3d  root=%-4d h=%-3d bf=%+d\n",
               keys[i], root->data, root->height, balanceFactor(root));
    }

    printf("\nInorder  (data, height, balance factor):\n  ");
    avl_inorder(root);
    printf("\n");

    printf("Preorder (data, height, balance factor):\n  ");
    avl_preorder(root);
    printf("\n");

    printf("\nSearch 25 -> %s\n", avl_search(root, 25) ? "found" : "not found");
    printf("Search 99 -> %s\n",  avl_search(root, 99) ? "found" : "not found");

    /* Delete a node that triggers rebalancing */
    printf("\nDelete 40:\n");
    root = avl_delete(root, 40);
    printf("Inorder after delete:\n  ");
    avl_inorder(root);
    printf("\n");

    printf("\nDelete 10:\n");
    root = avl_delete(root, 10);
    printf("Inorder after delete:\n  ");
    avl_inorder(root);
    printf("\n");

    freeAVL(root);
    return 0;
}
