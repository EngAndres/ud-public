/* ============================================================
 * Red-Black Tree
 *
 * Properties enforced:
 *   1. Every node is RED or BLACK.
 *   2. The root is BLACK.
 *   3. Every leaf (nil sentinel) is BLACK.
 *   4. Red nodes have only BLACK children.
 *   5. Every path from a node to its descendant nil-leaves
 *      has the same number of black nodes (black-height).
 *
 * Uses a single shared nil sentinel (Cormen / CLRS style).
 * Operations: insert, delete, search + inorder / preorder.
 * ============================================================ */
#include <stdio.h>
#include <stdlib.h>

#define RED   0
#define BLACK 1

/* ── Node ──────────────────────────────────────────────────── */
typedef struct RBNode {
    int data;
    int color;                       /* RED | BLACK */
    struct RBNode *left, *right, *parent;
} RBNode;

typedef struct {
    RBNode *root;
    RBNode *nil;                     /* shared sentinel leaf */
} RBTree;

/* ── Constructor / destructor ──────────────────────────────── */
RBTree *rb_create(void) {
    RBTree *t    = malloc(sizeof(RBTree));
    t->nil        = malloc(sizeof(RBNode));
    t->nil->color = BLACK;
    t->nil->left  = t->nil->right = t->nil->parent = NULL;
    t->root       = t->nil;
    return t;
}

static RBNode *rbNewNode(RBTree *t, int data) {
    RBNode *n    = malloc(sizeof(RBNode));
    n->data       = data;
    n->color      = RED;
    n->left = n->right = n->parent = t->nil;
    return n;
}

/* ── Rotations ─────────────────────────────────────────────── */
/*
 *   x              y
 *  / \    Left    / \
 * T1  y  ----->  x   T3
 *    / \        / \
 *   T2 T3      T1 T2
 */
static void leftRotate(RBTree *t, RBNode *x) {
    RBNode *y  = x->right;
    x->right   = y->left;
    if (y->left != t->nil)
        y->left->parent = x;

    y->parent = x->parent;
    if      (x->parent == t->nil)        t->root         = y;
    else if (x == x->parent->left)       x->parent->left  = y;
    else                                 x->parent->right = y;

    y->left    = x;
    x->parent  = y;
}

/*
 *     y              x
 *    / \   Right    / \
 *   x  T3  ----->  T1  y
 *  / \                / \
 * T1 T2              T2 T3
 */
static void rightRotate(RBTree *t, RBNode *y) {
    RBNode *x  = y->left;
    y->left    = x->right;
    if (x->right != t->nil)
        x->right->parent = y;

    x->parent = y->parent;
    if      (y->parent == t->nil)        t->root          = x;
    else if (y == y->parent->right)      y->parent->right  = x;
    else                                 y->parent->left   = x;

    x->right   = y;
    y->parent  = x;
}

/* ── Insert fix-up ─────────────────────────────────────────── */
/*
 * After a RED node z is inserted its RED parent may violate
 * property 4.  Three cases (mirrored for right-side parent):
 *   Case 1: Uncle is RED       — recolour, move z up
 *   Case 2: Uncle is BLACK, z is inner child — rotate parent
 *   Case 3: Uncle is BLACK, z is outer child — rotate grandpa
 */
static void rbInsertFix(RBTree *t, RBNode *z) {
    while (z->parent->color == RED) {
        if (z->parent == z->parent->parent->left) {
            RBNode *uncle = z->parent->parent->right;

            if (uncle->color == RED) {                 /* Case 1 */
                z->parent->color         = BLACK;
                uncle->color             = BLACK;
                z->parent->parent->color = RED;
                z = z->parent->parent;
            } else {
                if (z == z->parent->right) {           /* Case 2 */
                    z = z->parent;
                    leftRotate(t, z);
                }
                z->parent->color         = BLACK;      /* Case 3 */
                z->parent->parent->color = RED;
                rightRotate(t, z->parent->parent);
            }
        } else {                                       /* mirror */
            RBNode *uncle = z->parent->parent->left;

            if (uncle->color == RED) {                 /* Case 1 */
                z->parent->color         = BLACK;
                uncle->color             = BLACK;
                z->parent->parent->color = RED;
                z = z->parent->parent;
            } else {
                if (z == z->parent->left) {            /* Case 2 */
                    z = z->parent;
                    rightRotate(t, z);
                }
                z->parent->color         = BLACK;      /* Case 3 */
                z->parent->parent->color = RED;
                leftRotate(t, z->parent->parent);
            }
        }
    }
    t->root->color = BLACK;   /* property 2 */
}

void rb_insert(RBTree *t, int data) {
    RBNode *z = rbNewNode(t, data);
    RBNode *y = t->nil, *x = t->root;

    while (x != t->nil) {
        y = x;
        if      (z->data < x->data) x = x->left;
        else if (z->data > x->data) x = x->right;
        else { free(z); return; }   /* duplicate: ignore */
    }
    z->parent = y;
    if      (y == t->nil)          t->root  = z;
    else if (z->data < y->data)    y->left  = z;
    else                           y->right = z;

    rbInsertFix(t, z);
}

/* ── Delete helpers ────────────────────────────────────────── */
static void rbTransplant(RBTree *t, RBNode *u, RBNode *v) {
    if      (u->parent == t->nil)       t->root          = v;
    else if (u == u->parent->left)      u->parent->left  = v;
    else                                u->parent->right = v;
    v->parent = u->parent;
}

static RBNode *rbMin(RBTree *t, RBNode *x) {
    while (x->left != t->nil) x = x->left;
    return x;
}

/* ── Delete fix-up ─────────────────────────────────────────── */
/*
 * x is a "doubly black" node that needs to shed one black.
 * Four cases (mirrored):
 *   Case 1: Sibling w is RED          — rotate parent
 *   Case 2: w's children are both BLACK — recolour w, move up
 *   Case 3: w's far child is BLACK     — rotate sibling
 *   Case 4: w's far child is RED       — rotate parent, done
 */
static void rbDeleteFix(RBTree *t, RBNode *x) {
    while (x != t->root && x->color == BLACK) {
        if (x == x->parent->left) {
            RBNode *w = x->parent->right;

            if (w->color == RED) {                          /* Case 1 */
                w->color           = BLACK;
                x->parent->color   = RED;
                leftRotate(t, x->parent);
                w = x->parent->right;
            }
            if (w->left->color == BLACK && w->right->color == BLACK) {
                w->color = RED;                             /* Case 2 */
                x = x->parent;
            } else {
                if (w->right->color == BLACK) {             /* Case 3 */
                    w->left->color = BLACK;
                    w->color       = RED;
                    rightRotate(t, w);
                    w = x->parent->right;
                }
                w->color           = x->parent->color;     /* Case 4 */
                x->parent->color   = BLACK;
                w->right->color    = BLACK;
                leftRotate(t, x->parent);
                x = t->root;
            }
        } else {                                            /* mirror */
            RBNode *w = x->parent->left;

            if (w->color == RED) {                          /* Case 1 */
                w->color           = BLACK;
                x->parent->color   = RED;
                rightRotate(t, x->parent);
                w = x->parent->left;
            }
            if (w->right->color == BLACK && w->left->color == BLACK) {
                w->color = RED;                             /* Case 2 */
                x = x->parent;
            } else {
                if (w->left->color == BLACK) {              /* Case 3 */
                    w->right->color = BLACK;
                    w->color        = RED;
                    leftRotate(t, w);
                    w = x->parent->left;
                }
                w->color           = x->parent->color;     /* Case 4 */
                x->parent->color   = BLACK;
                w->left->color     = BLACK;
                rightRotate(t, x->parent);
                x = t->root;
            }
        }
    }
    x->color = BLACK;
}

void rb_delete(RBTree *t, int data) {
    /* find node */
    RBNode *z = t->root;
    while (z != t->nil) {
        if      (data == z->data) break;
        else if (data  < z->data) z = z->left;
        else                      z = z->right;
    }
    if (z == t->nil) return;   /* not found */

    RBNode *y = z, *x;
    int origColor = y->color;

    if (z->left == t->nil) {
        x = z->right;
        rbTransplant(t, z, z->right);
    } else if (z->right == t->nil) {
        x = z->left;
        rbTransplant(t, z, z->left);
    } else {
        y         = rbMin(t, z->right);
        origColor = y->color;
        x         = y->right;
        if (y->parent == z) {
            x->parent = y;
        } else {
            rbTransplant(t, y, y->right);
            y->right         = z->right;
            y->right->parent = y;
        }
        rbTransplant(t, z, y);
        y->left         = z->left;
        y->left->parent = y;
        y->color        = z->color;
    }
    free(z);
    if (origColor == BLACK)
        rbDeleteFix(t, x);
}

/* ── Search ────────────────────────────────────────────────── */
RBNode *rb_search(RBTree *t, int data) {
    RBNode *cur = t->root;
    while (cur != t->nil) {
        if      (data == cur->data) return cur;
        else if (data  < cur->data) cur = cur->left;
        else                        cur = cur->right;
    }
    return NULL;
}

/* ── Traversals ────────────────────────────────────────────── */
static const char *colorStr(int c) { return c == RED ? "R" : "B"; }

void rb_inorder(RBTree *t, RBNode *n) {
    if (n == t->nil) return;
    rb_inorder(t, n->left);
    printf("%d(%s) ", n->data, colorStr(n->color));
    rb_inorder(t, n->right);
}

void rb_preorder(RBTree *t, RBNode *n) {
    if (n == t->nil) return;
    printf("%d(%s) ", n->data, colorStr(n->color));
    rb_preorder(t, n->left);
    rb_preorder(t, n->right);
}

/* ── Verification helpers ──────────────────────────────────── */
/* Black-height: number of black nodes on any path to a nil leaf
   (not counting the node itself). Returns -1 if violated.     */
static int blackHeight(RBTree *t, RBNode *n) {
    if (n == t->nil) return 0;
    int lbh = blackHeight(t, n->left);
    int rbh = blackHeight(t, n->right);
    if (lbh < 0 || rbh < 0 || lbh != rbh) return -1;
    return lbh + (n->color == BLACK ? 1 : 0);
}

/* Check property 4: no consecutive red nodes */
static int noConsecRed(RBTree *t, RBNode *n) {
    if (n == t->nil) return 1;
    if (n->color == RED) {
        if (n->left->color  == RED) return 0;
        if (n->right->color == RED) return 0;
    }
    return noConsecRed(t, n->left) && noConsecRed(t, n->right);
}

static void verifyRB(RBTree *t) {
    int bh = blackHeight(t, t->root);
    int ok = (t->root->color == BLACK) &&
             noConsecRed(t, t->root)   &&
             (bh >= 0);
    printf("RB properties: %s  (black-height = %d)\n",
           ok ? "OK" : "VIOLATED", bh < 0 ? -1 : bh);
}

/* ── Free ──────────────────────────────────────────────────── */
static void rbFreeNodes(RBTree *t, RBNode *n) {
    if (n == t->nil) return;
    rbFreeNodes(t, n->left);
    rbFreeNodes(t, n->right);
    free(n);
}

void rb_destroy(RBTree *t) {
    rbFreeNodes(t, t->root);
    free(t->nil);
    free(t);
}

/* ── Demo ──────────────────────────────────────────────────── */
int main(void) {
    RBTree *t = rb_create();
    int keys[] = {10, 20, 30, 15, 25, 5, 1, 35, 28};
    int n = (int)(sizeof(keys) / sizeof(keys[0]));

    printf("=== Red-Black Tree ===\n\n");
    printf("%-12s %-10s %s\n", "Operation", "Root", "Verify");
    printf("------------------------------------------\n");

    for (int i = 0; i < n; i++) {
        rb_insert(t, keys[i]);
        int bh = blackHeight(t, t->root);
        printf("insert %-4d  root=%-4d(B)  BH=%d\n",
               keys[i], t->root->data, bh);
    }

    printf("\nInorder  (sorted, shows colors):\n  ");
    rb_inorder(t, t->root);
    printf("\n");

    printf("Preorder (shows tree shape):\n  ");
    rb_preorder(t, t->root);
    printf("\n\n");

    verifyRB(t);

    printf("\nSearch 25 -> %s\n", rb_search(t, 25) ? "found" : "not found");
    printf("Search 99 -> %s\n",  rb_search(t, 99) ? "found" : "not found");

    printf("\nDelete 20 (root or internal node):\n");
    rb_delete(t, 20);
    printf("Inorder: "); rb_inorder(t, t->root); printf("\n");
    verifyRB(t);

    printf("\nDelete 1 (leaf):\n");
    rb_delete(t, 1);
    printf("Inorder: "); rb_inorder(t, t->root); printf("\n");
    verifyRB(t);

    printf("\nDelete 10:\n");
    rb_delete(t, 10);
    printf("Inorder: "); rb_inorder(t, t->root); printf("\n");
    verifyRB(t);

    rb_destroy(t);
    return 0;
}
