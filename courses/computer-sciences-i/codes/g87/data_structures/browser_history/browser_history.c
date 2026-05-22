/*
This file has a simple implementation of a browser history using a
doubly-linked list as the underlying data structure.

It includes basic operations such as visiting a URL, going back,
going forward, and freeing the history.

Going back/forward is O(1) by following prev/next pointers.
Visiting a new URL truncates the forward history. The program also
provides a menu-driven interface for users to interact with the
browser history.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define URL_MAX 256

/* Node definition */
typedef struct WebPage {
    char url[URL_MAX]; //String
    struct WebPage *prev;
    struct WebPage *next;
} WebPage;

/* Handle */
typedef struct {
    WebPage *current;
    int size;
} BrowserHistory;

/* Helpers */
static WebPage *new_page(const char *url) {
    WebPage *p = malloc(sizeof(WebPage));
    if (!p) { 
        perror("Memory allocation failed."); 
        exit(EXIT_FAILURE); 
    }
    
    strncpy(p->url, url, URL_MAX - 1);
    p->url[URL_MAX - 1] = '\0';
    p->prev = p->next = NULL;
    return p;
}

/* Free every node from `start` to the end of the forward chain */
static void free_forward(WebPage *start) {
    while (start) {
        WebPage *tmp = start->next;
        free(start);
        start = tmp;
    }
}

void history_init(BrowserHistory *h) {
    h->current = NULL;
    h->size = 0;
}

/* Operations */

/* Visit a new URL: truncate any forward history, then append — O(1) */
void visit(BrowserHistory *h, const char *url) {
    WebPage *p = new_page(url);

    if (h->current) {
        /* Truncate forward chain (forward history is discarded) */
        WebPage *fwd = h->current->next;
        while (fwd) { 
            WebPage *tmp = fwd->next; 
            free(fwd); fwd = tmp; 
            h->size--; 
        }
        h->current->next = p;
        p->prev = h->current;
    }
    h->current = p;
    h->size++;
    printf("  Visited : %s\n", url);
}

/* Go back one page — O(1) */
void go_back(BrowserHistory *h) {
    if (!h->current || !h->current->prev) {
        puts("  go_back: already at the oldest page");
        return;
    }
    h->current = h->current->prev;
    printf("  Back    : %s\n", h->current->url);
}

/* Go forward one page — O(1) */
void go_forward(BrowserHistory *h) {
    if (!h->current || !h->current->next) {
        puts("  go_forward: already at the newest page");
        return;
    }
    h->current = h->current->next;
    printf("  Forward : %s\n", h->current->url);
}

/* Free all nodes regardless of current position */
void free_history(BrowserHistory *h) {
    /* Walk to the head first */
    if (!h->current) 
        return;
    WebPage *head = h->current;
    
    while (head->prev) 
        head = head->prev;
    free_forward(head);
    h->current = NULL;
    h->size = 0;
}

/* Print the full history; mark the current page */
void print_history(const BrowserHistory *h) {
    if (!h->current) { 
        puts("  (no history)"); 
        return; 
    }

    /* Walk to head */
    const WebPage *node = h->current;
    while (node->prev) 
        node = node->prev;

    printf("  History : ");
    while (node) {
        if (node == h->current)
            printf("[*%s] ", node->url);
        else
            printf("[%s] ", node->url);
        node = node->next;
    }
    printf("\n");
}

/* main */
void print_menu(void) {
    printf("\n\n\t\tMENU\n");
    printf("1. Visit URL\n");
    printf("2. Go Back\n");
    printf("3. Go Forward\n");
    printf("4. Print History\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    BrowserHistory h;
    history_init(&h);
    int option;
    char url[URL_MAX];

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Enter URL: ");
                scanf("%255s", url);
                visit(&h, url);
                break;
            case 2:
                go_back(&h);
                break;
            case 3:
                go_forward(&h);
                break;
            case 4:
                print_history(&h);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    free_history(&h);
    return 0;
}
