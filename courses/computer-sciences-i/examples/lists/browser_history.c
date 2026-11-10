#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Page {
    char title[100];
    char url[50];
    char date[20];
    struct Page *next;
    struct Page *prev;
} Page;


typedef struct BrowserHistory{
    Page *head;
    Page *tail; // last item in the list
    Page *current; // navigation purposes
} BrowserHistory;


void initHistory(BrowserHistory *history){
    history->head = NULL;
    history->tail = NULL;
    history->current = NULL;
}

// Equivalente to add a new page to the history
void visiteWebSite(BrowserHistory *history, char title[], 
                    char url[], char date[]){
    //Visiting a new page, first save data structure
    Page *new_page = malloc( sizeof(Page) );
    if(new_page == NULL){
        puts("No es posible crear espacio en la memoria para la nueva pagina.");
        return;
    }
    strcpy(new_page->title, title);
    strcpy(new_page->url, url);
    strcpy(new_page->date, date);

    if(history->current == NULL){
        //empty history
        history->head = new_page;
        history->tail = new_page;
        history->current = new_page;
        return;
    }

    // if current in the middle, lost forward
    Page *temp = history->current->next;
    while(temp != NULL){
        Page *next_page = temp->next;
        free(temp);
        temp = next_page;
    }
}

void goBack(BrowserHistory *history){
    if(history->head == NULL) {
        puts("No se puede ir hacia atrás porque historial es vacío.");
        return;
    }
    if(history->current->prev == NULL) { //First elemento of the history
        puts("Actualmente está en la primera página del historial.");
        return;
    }
    history->current = history->current->prev;
} 

void goForward(BrowserHistory *history){
    if(history->head == NULL) {
        puts("No se puede ir hacia adelante porque historial es vacío.");
        return;
    }
    if(history->current->next == NULL) { //Last element of the history
        puts("Actualmente está en la última página del historial.");
        return;
    }
    history->current = history->current->next;
} 

Page *searchPage(BrowserHistory *history, char url[]){
    Page *cur = history->head;

    while(cur != NULL){
        if(strcmp(cur->url, url) == 0){
            return cur; // Found
        }
        cur = cur->next;
    }

    return NULL;
}

Page[] last5pages(BrowserHistory *history){
    Page pages[5];
    Page *cur = history->tail;
    for(int i = 0; i < 5; i++){
        if(cur == NULL)
            break;
        pages[i] = cur;
        cur = cur->prev;
    }
    return pages;
}