/*
This file has a simple implementation of a music playlist using a
singly linked list as the underlying data structure.

It includes basic operations such as inserting a song at the end,
deleting by title or position, searching by title or artist,
playing the next song, and shuffling the playlist.

Shuffling uses a Fisher-Yates approach over a node-pointer array.
The program also provides a menu-driven interface for users to
interact with the playlist.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

/* ADJUSTMENTS:
1. In new_song, title and artist were assigned by pointer without
   copying the string data. Fixed with malloc(strlen+1) + strcpy.
2. new_song was missing s->next = NULL, causing undefined behaviour
   when traversing the list.
3. lineal_search_by_title and lineal_search_by_artist used == for
   string comparison (pointer equality). Fixed with strcmp(...) == 0.
4. print_playlist used integer division (/ 60) with a %.1f format
   specifier. Fixed by dividing by 60.0.
5. find_previous had return type void* instead of Song*.
6. shuffle_list reimplemented with Fisher-Yates on a node-pointer
   array to avoid pointer aliasing bugs in the original swap logic.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct Song {
    char *title;
    int duration_seconds;
    char *artist;
    struct Song *next;
} Song;

typedef struct {
    Song *head;
    Song *current;
    int size;
} Playlist;


/* Basic Functions */
static Song *new_song(char *new_title, int new_duration, char *new_artist) {
    Song *s = malloc(sizeof(Song));
    if (!s) {
        perror("Malloc Failed.");
        exit(EXIT_FAILURE);
    }
    s->title = malloc(strlen(new_title) + 1);
    strcpy(s->title, new_title);
    s->artist = malloc(strlen(new_artist) + 1);
    strcpy(s->artist, new_artist);
    s->duration_seconds = new_duration;
    s->next = NULL;
    return s;
}

void list_init(Playlist *list) {
    list->head = NULL;
    list->current = NULL;
    list->size = 0;
}

/* Insertions */
void insert(Playlist *list, Song *song) {
    if (!list->head) {
        list->head = song;
    } else {
        Song *cur = list->head;
        while (cur->next)
            cur = cur->next;
        cur->next = song;
    }
    list->size++;
}

/* Searches */
int lineal_search_by_title(const Playlist *list, char *title) {
    Song *cur = list->head;
    int index = 0;
    while (cur) {
        if (strcmp(cur->title, title) == 0)
            return index;
        cur = cur->next;
        index++;
    }
    return -1;
}

int lineal_search_by_artist(const Playlist *list, char *artist) {
    Song *cur = list->head;
    int index = 0;
    while (cur) {
        if (strcmp(cur->artist, artist) == 0)
            return index;
        cur = cur->next;
        index++;
    }
    return -1;
}

/* Deletions */
static void private_delete_begin(Playlist *list) {
    if (!list->head) {
        puts("delete_begin: cannot delete from an empty list.");
        return;
    }
    Song *temp = list->head;
    list->head = temp->next;
    free(temp->title);
    free(temp->artist);
    free(temp);
    list->size--;
}

void delete_middle(Playlist *list, int position) {
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
    free(temp->title);
    free(temp->artist);
    free(temp);
    list->size--;
}

void delete_by_title(Playlist *list, char *title) {
    int index = lineal_search_by_title(list, title);
    if (index == -1)
        printf("Title '%s' not found.\n", title);
    else
        delete_middle(list, index);
}

/* Utilities */
void print_playlist(const Playlist *list) {
    if (!list->head) {
        puts("Playlist is empty.");
        return;
    }
    printf("\tHEAD\n");
    Song *song = list->head;
    while (song) {
        printf("Title: %s\tArtist: %s\tDuration: %.1f min\n",
               song->title, song->artist, song->duration_seconds / 60.0);
        song = song->next;
    }
    printf("\tTAIL.\n");
    printf("Size: %d\n\n", list->size);
}

void list_free(Playlist *list) {
    Song *song = list->head;
    while (song) {
        Song *temp = song->next;
        free(song->title);
        free(song->artist);
        free(song);
        song = temp;
    }
    list->head = NULL;
    list->current = NULL;
    list->size = 0;
}

/* Playlist controls */
void play_next(Playlist *list) {
    if (!list->current) {
        if (list->head) {
            list->current = list->head;
            printf("Now playing: %s - %s\n",
                   list->current->title, list->current->artist);
        } else {
            puts("Cannot play an empty playlist. Add a song first.");
        }
        return;
    }
    if (!list->current->next) {
        list->current = NULL;
        puts("End of playlist.");
        return;
    }
    list->current = list->current->next;
    printf("Now playing: %s - %s\n",
           list->current->title, list->current->artist);
}

Song *find_previous(Playlist *list, int position) {
    Song *prev = list->head;
    for (int i = 0; i < position - 1; i++)
        prev = prev->next;
    return prev;
}

void shuffle_list(Playlist *list) {
    if (list->size < 2) return;
    srand((unsigned)time(NULL));

    Song **nodes = malloc(list->size * sizeof(Song *));
    if (!nodes) { perror("Malloc Failed."); return; }

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
    list->current = NULL;
    free(nodes);
}

/* Menu */
void print_menu() {
    printf("\n\n\t\tMENU\n");
    printf("1. Add Song\n");
    printf("2. Remove Song by Title\n");
    printf("3. Play Next\n");
    printf("4. Shuffle Playlist\n");
    printf("5. Search by Title\n");
    printf("6. Search by Artist\n");
    printf("7. Print Playlist\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    Playlist list;
    list_init(&list);
    int option;
    char title[100];
    char artist[100];
    int duration;
    int found;

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Song title: ");
                scanf(" %99[^\n]", title);
                printf("Artist: ");
                scanf(" %99[^\n]", artist);
                printf("Duration (seconds): ");
                scanf("%d", &duration);
                insert(&list, new_song(title, duration, artist));
                break;
            case 2:
                printf("Title to remove: ");
                scanf(" %99[^\n]", title);
                delete_by_title(&list, title);
                break;
            case 3:
                play_next(&list);
                break;
            case 4:
                shuffle_list(&list);
                puts("Playlist shuffled.");
                break;
            case 5:
                printf("Title to search: ");
                scanf(" %99[^\n]", title);
                found = 0;
                {
                    Song *cur = list.head;
                    int idx = 0;
                    while (cur) {
                        if (strcmp(cur->title, title) == 0) {
                            printf("[%d] Title: %s | Artist: %s | Duration: %.1f min\n",
                                   idx, cur->title, cur->artist,
                                   cur->duration_seconds / 60.0);
                            found = 1;
                        }
                        cur = cur->next;
                        idx++;
                    }
                }
                if (!found)
                    printf("'%s' not found.\n", title);
                break;
            case 6:
                printf("Artist to search: ");
                scanf(" %99[^\n]", artist);
                found = 0;
                {
                    Song *cur = list.head;
                    int idx = 0;
                    while (cur) {
                        if (strcmp(cur->artist, artist) == 0) {
                            printf("[%d] Title: %s | Artist: %s | Duration: %.1f min\n",
                                   idx, cur->title, cur->artist,
                                   cur->duration_seconds / 60.0);
                            found = 1;
                        }
                        cur = cur->next;
                        idx++;
                    }
                }
                if (!found)
                    printf("Artist '%s' not found.\n", artist);
                break;
            case 7:
                print_playlist(&list);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }
    } while (option != 0);

    list_free(&list);
    return 0;
}
