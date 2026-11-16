/*
 * browser_history.c
 *
 * Simulación del historial de navegación de un navegador web usando una
 * lista doblemente enlazada. Cada nodo (Page) representa una página visitada
 * y el historial mantiene un puntero a la página actual para poder moverse
 * hacia atrás y hacia adelante.
 *
 * Compilar:  gcc -Wall -Wextra -std=c99 browser_history.c -o browser_history
 * Ejecutar:  ./browser_history
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * Página web almacenada en el historial.
 *
 * title : título de la página.
 * url   : dirección de la página.
 * date  : fecha en que se visitó.
 * next  : página siguiente en el historial (más reciente).
 * prev  : página anterior en el historial (más antigua).
 */
typedef struct Page {
    char title[100];
    char url[50];
    char date[20];
    struct Page *next;
    struct Page *prev;
} Page;


/**
 * Historial del navegador.
 *
 * head    : primera página del historial.
 * tail    : última página del historial.
 * current : página que se está mostrando actualmente.
 */
typedef struct BrowserHistory{
    Page *head;
    Page *tail;     // última página de la lista
    Page *current;  // página actual, para la navegación
} BrowserHistory;


/**
 * Inicializa un historial vacío.
 *
 * @param history  puntero al historial a inicializar.
 */
void initHistory(BrowserHistory *history){
    history->head = NULL;
    history->tail = NULL;
    history->current = NULL;
}

/**
 * Visita una nueva página. Equivale a agregar una página al historial.
 * Si el usuario había retrocedido, se eliminan las páginas "hacia adelante"
 * antes de agregar la nueva.
 *
 * @param history  historial donde se registra la visita.
 * @param title    título de la página.
 * @param url      dirección de la página.
 * @param date     fecha de la visita.
 */
void visiteWebSite(BrowserHistory *history, char title[],
                    char url[], char date[]){
    // Se reserva memoria para la nueva página
    Page *new_page = malloc( sizeof(Page) );
    if(new_page == NULL){
        puts("No es posible crear espacio en la memoria para la nueva pagina.");
        return;
    }
    strcpy(new_page->title, title);
    strcpy(new_page->url, url);
    strcpy(new_page->date, date);
    new_page->next = NULL;
    new_page->prev = NULL;

    // Historial vacío: la nueva página es la única
    if(history->current == NULL){
        history->head = new_page;
        history->tail = new_page;
        history->current = new_page;
        return;
    }

    // Si la página actual está en medio, se pierde el historial hacia adelante
    Page *temp = history->current->next;
    while(temp != NULL){
        Page *next_page = temp->next;
        free(temp);
        temp = next_page;
    }

    // Se enlaza la nueva página después de la actual
    history->current->next = new_page;
    new_page->prev = history->current;
    history->current = new_page;
    history->tail = new_page;
}

/**
 * Retrocede a la página anterior del historial.
 * Si ya está en la primera página, muestra un mensaje y no hace nada.
 *
 * @param history  historial en el que se navega.
 */
void goBack(BrowserHistory *history){
    if(history->head == NULL) {
        puts("No se puede ir hacia atrás porque historial es vacío.");
        return;
    }
    if(history->current->prev == NULL) { // primera página del historial
        puts("Actualmente está en la primera página del historial.");
        return;
    }
    history->current = history->current->prev;
}

/**
 * Avanza a la página siguiente del historial.
 * Si ya está en la última página, muestra un mensaje y no hace nada.
 *
 * @param history  historial en el que se navega.
 */
void goForward(BrowserHistory *history){
    if(history->head == NULL) {
        puts("No se puede ir hacia adelante porque historial es vacío.");
        return;
    }
    if(history->current->next == NULL) { // última página del historial
        puts("Actualmente está en la última página del historial.");
        return;
    }
    history->current = history->current->next;
}

/**
 * Busca una página en el historial por su URL.
 *
 * @param history  historial donde se busca.
 * @param url      dirección a buscar.
 * @return         puntero a la página encontrada, o NULL si no existe.
 */
Page *searchPage(BrowserHistory *history, char url[]){
    Page *cur = history->head;

    while(cur != NULL){
        if(strcmp(cur->url, url) == 0){
            return cur; // encontrada
        }
        cur = cur->next;
    }

    return NULL;
}

/**
 * Obtiene una subcopia con las últimas 5 páginas del historial, de la más
 * antigua a la más reciente.
 *
 * El arreglo es 'static' porque una variable local no puede devolverse en C.
 * Por eso cada llamada sobrescribe el resultado de la anterior.
 *
 * @param history  historial del que se copian las páginas.
 * @param count    salida: cantidad de páginas copiadas (entre 0 y 5).
 * @return         arreglo con las copias de las páginas.
 */
Page *last5pages(BrowserHistory *history, int *count){
    static Page pages[5];
    Page *cur = history->tail;
    int i;

    for(i = 0; i < 5; i++){
        if(cur == NULL) break;
        pages[i] = *cur; // copia de la página
        cur = cur->prev;
    }
    *count = i;
    return pages;
}

/**
 * Limpia el historial del navegador: libera la memoria de todas las
 * páginas y deja el historial vacío. Puede usarse también para liberar
 * la memoria al terminar el programa.
 *
 * @param history  historial a limpiar.
 */
void clearHistory(BrowserHistory *history){
    Page *cur = history->head;

    while(cur != NULL){
        Page *next_page = cur->next;
        free(cur);
        cur = next_page;
    }

    history->head = NULL;
    history->tail = NULL;
    history->current = NULL;
    puts("Historial del navegador limpiado.");
}

/**
 * Muestra en pantalla los datos de una página.
 *
 * @param page  página a mostrar; si es NULL no imprime nada.
 */
void printPage(const Page *page){
    if(page == NULL) return;
    printf("Título: %s\nURL: %s\nFecha: %s\n",
           page->title, page->url, page->date);
}

/**
 * Muestra la página actual del navegador.
 *
 * @param history  historial del navegador.
 */
void showCurrentPage(BrowserHistory *history){
    if(history->current == NULL){
        puts("No hay ninguna página abierta.");
        return;
    }
    puts("--- Página actual ---");
    printPage(history->current);
}

/**
 * Lee una línea de texto desde la entrada estándar y quita el salto de línea.
 *
 * @param buffer  donde se guarda la línea leída.
 * @param size    tamaño del buffer.
 * @return        1 si se leyó correctamente, 0 si hubo fin de entrada.
 */
int readLine(char buffer[], int size){
    if(fgets(buffer, size, stdin) == NULL){
        buffer[0] = '\0';
        return 0;
    }
    buffer[strcspn(buffer, "\n")] = '\0';
    return 1;
}

/**
 * Muestra el menú principal del navegador.
 */
void showMenu(void){
    puts("\n===== NAVEGADOR WEB =====");
    puts("1. Visitar una página");
    puts("2. Ir hacia atrás");
    puts("3. Ir hacia adelante");
    puts("4. Ver página actual");
    puts("5. Buscar página por URL");
    puts("6. Ver últimas 5 páginas");
    puts("7. Limpiar historial");
    puts("0. Salir");
    printf("Opción: ");
}

/**
 * Lee la opción elegida por el usuario en el menú.
 *
 * @return  número de la opción; -1 si el texto no es un número válido;
 *          0 si no se pudo leer (fin de entrada).
 */
int readOption(void){
    char buffer[16];
    char *end;
    long value;

    if(!readLine(buffer, sizeof(buffer))) return 0;

    value = strtol(buffer, &end, 10);
    if(end == buffer || *end != '\0') return -1; // no es un número
    return (int)value;
}

/**
 * Punto de entrada del programa: muestra el menú y ejecuta la opción
 * seleccionada hasta que el usuario elija salir.
 *
 * @return  0 si el programa termina correctamente.
 */
int main(void){
    BrowserHistory history;
    char title[100], url[50], date[20];
    int option;

    initHistory(&history);

    do {
        showMenu();
        option = readOption();

        switch(option){
            case 1:
                printf("Título: ");
                readLine(title, sizeof(title));
                printf("URL: ");
                readLine(url, sizeof(url));
                printf("Fecha: ");
                readLine(date, sizeof(date));
                visiteWebSite(&history, title, url, date);
                break;

            case 2:
                goBack(&history);
                showCurrentPage(&history);
                break;

            case 3:
                goForward(&history);
                showCurrentPage(&history);
                break;

            case 4:
                showCurrentPage(&history);
                break;

            case 5: {
                Page *found;
                printf("URL a buscar: ");
                readLine(url, sizeof(url));
                found = searchPage(&history, url);
                if(found != NULL){
                    puts("Página encontrada:");
                    printPage(found);
                } else {
                    puts("La página no está en el historial.");
                }
                break;
            }

            case 6: {
                Page *last;
                int count;
                last = last5pages(&history, &count);
                if(count == 0){
                    puts("El historial está vacío.");
                }
                for(int i = 0; i < count; i++){
                    printf("\n%d. ", i + 1);
                    printPage(&last[i]);
                }
                break;
            }

            case 7:
                clearHistory(&history);
                break;

            case 0:
                puts("Cerrando el navegador...");
                break;

            default:
                puts("Opción no válida, intente de nuevo.");
                break;
        }
    } while(option != 0);

    clearHistory(&history);
    return 0;
}
