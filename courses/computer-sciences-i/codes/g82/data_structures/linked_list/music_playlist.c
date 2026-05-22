/*
This file has a simple implementation of a music playlist using a
singly linked list as the underlying data structure.

It includes basic operations such as inserting a song at the end or
at a given position, deleting by position or by title, searching by
title or artist, playing the next song, and shuffling the playlist.

Shuffling uses a Fisher-Yates approach over a node-pointer array.
The program also provides a menu-driven interface for users to
interact with the playlist.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

/* ADJUSTMENTS:
1. In new_song, name and artist were assigned by pointer without
   copying the string data. Fixed with malloc(strlen+1) + strcpy;
   also added s->next = NULL.
2. linear_search_by_title and linear_search_by_artist used == for
   string comparison. Fixed with strcmp(...) == 0.
3. linear_search_previous returned a bare return on the error path
   of a non-void function. Fixed to return NULL.
4. shuffle_list reimplemented with Fisher-Yates on a node-pointer
   array to avoid pointer aliasing bugs from linear_search_previous.
5. delete_song: scanf("%s", option) -> scanf(" %c", &option);
   scanf("%d", position) -> scanf("%d", &position); uninitialized
   char* name replaced with a stack buffer; print() -> printf().
6. main: Playlist declared as an uninitialised pointer; fixed to a
   stack variable and init_list called with its address. Variables
   shared across switch cases moved before do-while. Stray printf
   lines inside switch removed. Cases 3-6 implemented.
7. print_playlist used integer division (/ 60) with %.1f format.
   Fixed by dividing by 60.0.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct Song {
    char *name;
    char *artist;
    int time_seconds;
    struct Song *next;
} Song;

typedef struct {
    Song *head;
    Song *current_play;
    int size;
} Playlist;


static Song *new_song(char *new_name, char *new_artist, int new_duration) {
    Song *s = malloc(sizeof(Song));
    if (!s) {
        perror("Malloc fails.");
        exit(EXIT_FAILURE);
    }
    s->name = malloc(strlen(new_name) + 1);
    strcpy(s->name, new_name);
    s->artist = malloc(strlen(new_artist) + 1);
    strcpy(s->artist, new_artist);
    s->time_seconds = new_duration;
    s->next = NULL;
    return s;
}

void init_list(Playlist *list) {
    list->head = NULL;
    list->current_play = NULL;
    list->size = 0;
}

/* INSERT */
void insert_end(Playlist *list, Song *song) {
    if (!list->head) {
        list->head = song;
    } else {
        Song *last = list->head;
        while (last->next)
            last = last->next;
        last->next = song;
    }
    list->size++;
}

void insert_position(Playlist *list, Song *song, int position) {
    if (position < 0 || position >= list->size) {
        fprintf(stderr, "insert_position: position %d out of range (size=%d)\n",
                position, list->size);
        return;
    }
    Song *current_node = list->head;
    for (int i = 0; i < position; i++)
        current_node = current_node->next;
    song->next = current_node->next;
    current_node->next = song;
    list->size++;
}

/* Searches */
int linear_search_by_title(Playlist *list, char *title) {
    Song *song = list->head;
    int index = 0;
    while (song) {
        if (strcmp(song->name, title) == 0)
            return index;
        song = song->next;
        index++;
    }
    return -1;
}

int linear_search_by_artist(Playlist *list, char *artist_) {
    Song *song = list->head;
    int index = 0;
    while (song) {
        if (strcmp(song->artist, artist_) == 0)
            return index;
        song = song->next;
        index++;
    }
    return -1;
}

Song *linear_search_previous(Playlist *list, int position) {
    if (position < 0 || position >= list->size) {
        fprintf(stderr,
                "linear_search_previous: index %d out of range (size=%d)\n",
                position, list->size);
        return NULL;
    }
    Song *previous = list->head;
    for (int i = 0; i < position - 1; i++)
        previous = previous->next;
    return previous;
}

/* Delete */
static void private_delete_begin(Playlist *list) {
    if (!list->head) {
        puts("List is empty. Cannot apply deletion.");
        return;
    }
    Song *temp = list->head;
    list->head = temp->next;
    free(temp->name);
    free(temp->artist);
    free(temp);
    list->size--;
}

void delete_position(Playlist *list, int position) {
    if (position < 0 || position >= list->size) {
        fprintf(stderr, "Index out of range: index %d, size %d.\n",
                position, list->size);
        return;
    }
    if (position == 0) {
        private_delete_begin(list);
        return;
    }
    Song *prev = list->head;
    for (int i = 0; i < position - 1; i++)
        prev = prev->next;
    Song *temp = prev->next;
    prev->next = temp->next;
    free(temp->name);
    free(temp->artist);
    free(temp);
    list->size--;
}

void delete_by_title(Playlist *list, char *title) {
    int index = linear_search_by_title(list, title);
    if (index != -1)
        delete_position(list, index);
    else
        fprintf(stderr, "Delete failure: song '%s' not in the list.\n", title);
}

/* Additionals */
void print_playlist(Playlist *list) {
    if (!list->head) {
        puts("Empty List.");
        return;
    }
    Song *song = list->head;
    printf(" HEAD\n");
    while (song) {
        printf("Title: %s\tArtist: %s\tDuration: %.1f minutes\n",
               song->name, song->artist, song->time_seconds / 60.0);
        song = song->next;
    }
    printf(" TAIL -> NULL, size=%d\n", list->size);
}

void free_memory(Playlist *list) {
    Song *temp = list->head;
    while (temp) {
        Song *next = temp->next;
        free(temp->name);
        free(temp->artist);
        free(temp);
        temp = next;
    }
    list->head = NULL;
}

/* Playlist functions */
void play_next(Playlist *list) {
    if (!list->current_play) {
        if (list->head) {
            list->current_play = list->head;
            printf("Now playing: %s - %s\n",
                   list->current_play->name, list->current_play->artist);
        } else {
            puts("You cannot play an empty playlist.");
        }
        return;
    }
    list->current_play = list->current_play->next;
    if (!list->current_play)
        puts("Playlist fully played.");
    else
        printf("Now playing: %s - %s\n",
               list->current_play->name, list->current_play->artist);
}

void shuffle_list(Playlist *list) {
    if (list->size < 2) return;
    srand((unsigned)time(NULL));

    Song **nodes = malloc(list->size * sizeof(Song *));
    if (!nodes) { 
        perror("Malloc fails."); 
        return; 
    }

    Song *cur = list->head;
    for (int i = 0; i < list->size; i++) {
        nodes[i] = cur;
        cur = cur->next;
    }
    for (int i = list->size - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        Song *tmp = nodes[i];
        nodes[i] = nodes[j];
        nodes[j] = tmp;
    }
    list->head = nodes[0];
    for (int i = 0; i < list->size - 1; i++)
        nodes[i]->next = nodes[i + 1];
    nodes[list->size - 1]->next = NULL;
    list->current_play = NULL;
    free(nodes);
}

void print_menu() {
    printf("\n\n\t\tMENU:\n");
    printf("1. Add Song\n");
    printf("2. Remove Song\n");
    printf("3. Play Next\n");
    printf("4. Shuffle List\n");
    printf("5. Search by Song\n");
    printf("6. Search by Artist\n");
    printf("7. Print Playlist\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

static void delete_song(Playlist *list) {
    char option;
    printf("Choose: p for position, t for title: ");
    scanf(" %c", &option);
    if (option == 'p') {
        int position;
        printf("Select a number between 0 and %d: ", list->size - 1);
        scanf("%d", &position);
        delete_position(list, position);
    } else if (option == 't') {
        char name[100];
        printf("Enter the name of the song: ");
        scanf(" %99[^\n]", name);
        delete_by_title(list, name);
    } else {
        printf("Invalid option for delete.\n");
    }
}

int main(void) {
    int option;
    Playlist list;
    init_list(&list);
    char name_t[100];
    char artist_t[100];
    int duration_t;
    int found;

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Song title: ");
                scanf(" %99[^\n]", name_t);
                printf("Artist: ");
                scanf(" %99[^\n]", artist_t);
                printf("Duration (seconds): ");
                scanf("%d", &duration_t);
                insert_end(&list, new_song(name_t, artist_t, duration_t));
                break;
            case 2:
                delete_song(&list);
                break;
            case 3:
                play_next(&list);
                break;
            case 4:
                shuffle_list(&list);
                puts("Playlist shuffled.");
                break;
            case 5:
                printf("Song title to search: ");
                scanf(" %99[^\n]", name_t);
                found = linear_search_by_title(&list, name_t);
                if (found == -1)
                    printf("'%s' not found.\n", name_t);
                else
                    printf("'%s' found at position %d.\n", name_t, found);
                break;
            case 6:
                printf("Artist to search: ");
                scanf(" %99[^\n]", artist_t);
                found = linear_search_by_artist(&list, artist_t);
                if (found == -1)
                    printf("Artist '%s' not found.\n", artist_t);
                else
                    printf("First song by '%s' at position %d.\n", artist_t, found);
                break;
            case 7:
                print_playlist(&list);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option. Choose a right option.\n");
        }
    } while (option != 0);

    free_memory(&list);
    return 0;
}
