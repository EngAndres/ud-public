/* This is an example of a playlist using a linked list.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Song {
    char title[50];
    char artist[50];
    int duration;
    Song *next;
} Song;

typedef struct Playlist {
    char name[50];
    Song *head;
    Song *current;
    int total_songs;
} Playlist;

// Create Nodes
Playlist *createPlaylist(char name[]){
    Playlist *new_playlist = malloc( sizeof(Playlist) );

    // Error if memory cannot be assigned
    if(new_playlist == NULL)
        return NULL;

    strcpy(new_playlist->name, name);
    new_playlist->head = NULL;
    new_playlist->current = NULL;
    new_playlist->total_songs = 0;

    return new_playlist;
}

Song *createSong(char title[], char artist[], int duration) {
    Song *new_song = malloc( sizeof(Song) );

    if(new_song == NULL)
        return NULL;

    strcpy(new_song->title, title);
    strcpy(new_song->artist, artist);
    new_song->duration = duration;

    return new_song;
}

// Insertion operations
void addSong(Playlist *playlist, char title[], char artist[], int duration){
    if(playlist == NULL)
        return;

    Song *song = createSong(title, artist, duration);
    if(song == NULL)
        return NULL;

    
    if(playlist->head = NULL){
        playlist->head = song;
        return;
    }

    Song *current = playlist->current;
    while(current->next != NULL){
        current = current->next;  
    }

    current->next =song; 
}


void addPlaylist(){

}