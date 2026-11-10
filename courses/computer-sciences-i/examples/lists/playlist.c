/* This is an example of a playlist using a linked list.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Nodo de cancion: lista enlazada simple dentro de cada playlist
typedef struct Song {
    char title[50];
    char artist[50];
    int duration;               // duracion en segundos
    struct Song *next;
} Song;

// Nodo de playlist: lista enlazada simple de playlists.
// Cada playlist contiene su propia lista enlazada de canciones.
typedef struct Playlist {
    char name[50];
    Song *head;                 // primera cancion
    Song *current;              // cancion actual (referencia auxiliar)
    int total_songs;            // numero de canciones de la playlist
    struct Playlist *next;
} Playlist;

// Create Nodes

// Crea una playlist vacia con el nombre indicado.
// Retorna el puntero a la nueva playlist, o NULL si no hay memoria.
Playlist *createPlaylist(char name[]){
    Playlist *new_playlist = malloc( sizeof(Playlist) );

    // Error if memory cannot be assigned
    if(new_playlist == NULL)
        return NULL;

    snprintf(new_playlist->name, sizeof(new_playlist->name), "%s", name);
    new_playlist->head = NULL;
    new_playlist->current = NULL;
    new_playlist->total_songs = 0;
    new_playlist->next = NULL;

    return new_playlist;
}

// Crea una cancion con titulo, artista y duracion (en segundos).
// Retorna el puntero a la nueva cancion, o NULL si no hay memoria.
Song *createSong(char title[], char artist[], int duration) {
    Song *new_song = malloc( sizeof(Song) );

    if(new_song == NULL)
        return NULL;

    snprintf(new_song->title, sizeof(new_song->title), "%s", title);
    snprintf(new_song->artist, sizeof(new_song->artist), "%s", artist);
    new_song->duration = duration;
    new_song->next = NULL;

    return new_song;
}

// Insertion operations

// Agrega una cancion al final de la playlist.
// Si la playlist es NULL o no hay memoria, no hace nada.
void addSong(Playlist *playlist, char title[], char artist[], int duration){
    if(playlist == NULL)
        return;

    Song *song = createSong(title, artist, duration);
    if(song == NULL)
        return;

    if(playlist->head == NULL){
        playlist->head = song;
        playlist->total_songs += 1;
        return;
    }

    Song *current = playlist->head;
    while(current->next != NULL){
        current = current->next;
    }

    current->next = song;
    playlist->total_songs += 1;
}

// Agrega una playlist al final de la lista de playlists.
// head_playlist es la direccion de la cabeza de la lista de playlists.
void addPlaylist(Playlist **head_playlist, char name[]){
    Playlist *new_playlist = createPlaylist(name);

    if(new_playlist == NULL)
        return;

    if(*head_playlist == NULL){
        *head_playlist = new_playlist;
        return;
    }

    Playlist *current = *head_playlist;
    while(current->next != NULL)
        current = current->next;

    current->next = new_playlist;
}

// Remove Song and Playlist by Name

// Elimina la primera cancion con el titulo indicado de la playlist.
// Si la cancion era la actual, reinicia la referencia current.
void deleteSong(Playlist *playlist, char name[]) {
    if(playlist == NULL || playlist->head == NULL)
        return;

    Song *current = playlist->head;
    Song *previous = NULL;

    while(current != NULL && strcmp(current->title, name) != 0){
        previous = current;
        current = current->next;
    }

    if(current == NULL){
        puts("Cancion no encontrada.");
        return;
    }

    if(previous == NULL){ //Song is the head
        playlist->head = current->next;
    } else {
        previous->next = current->next;
    }

    if(playlist->current == current)
        playlist->current = NULL;

    free(current); // borrado de la memoria
    puts("Cancion borrada exitosamente");
    playlist->total_songs -= 1;
}

// Cambia la duracion de la primera cancion con el titulo indicado.
void updateSong(Playlist *playlist, char name[], int new_duration) {
    if(playlist == NULL || playlist->head == NULL)
        return;

    Song *current = playlist->head;

    while(current != NULL && strcmp(current->title, name) != 0){
        current = current->next;
    }

    if(current == NULL){
        puts("Cancion no encontrada.");
        return;
    }

    current->duration = new_duration;
    puts("Cancion actualizado exitosamente");
}

// Busca una cancion por titulo y retorna una copia de ella.
// Si no existe, retorna una cancion con title vacio (title[0] == '\0').
Song findSong(Playlist *playlist, char name[]) {
    if(playlist == NULL || playlist->head == NULL){
        Song not_found = {0};
        return not_found;
    }

    Song *current = playlist->head;

    while(current != NULL && strcmp(current->title, name) != 0){
        current = current->next;
    }

    if(current == NULL){
        puts("Cancion no encontrada.");
        Song not_found = {0};
        return not_found;
    }

    puts("Cancion encontrada exitosamente");
    return *current;
}

// Search - Update - Delete a Playlist

// Elimina la playlist con el nombre indicado y libera sus canciones.
void deletePlaylist(Playlist **head_playlist, char name[]){
    Playlist *current = *head_playlist;
    Playlist *previous = NULL;

    while(current != NULL && strcmp(name, current->name) != 0){
        previous = current;
        current = current->next;
    }

    if(current == NULL){
        puts("Playlist no encontrada.");
        return;
    }

    if(previous == NULL) { //delete at the beggining
        *head_playlist = current->next;
    } else {
        previous->next = current->next;
    }

    Song *current_song = current->head;
    Song *song = NULL;
    while(current_song != NULL){
        song = current_song->next;
        free(current_song);
        current_song = song;
    }

    free(current);
    printf("La playlist %s ha sido exitosamente borrada.\n", name);
}

// Cambia el nombre de la playlist current_name por new_name.
void updatePlaylist(Playlist **head_playlist,
                            char current_name[], char new_name[]){
    Playlist *current = *head_playlist;
    while(current != NULL){
        if(strcmp(current->name, current_name) == 0){
            snprintf(current->name, sizeof(current->name), "%s", new_name);
            puts("Playlist actualizada correctamente");
            return;
        }
        current = current->next;
    }
    puts("Playlist no encontrada");
}

// Busca una playlist por nombre y retorna una copia de ella.
// Si no existe, retorna una playlist con name vacio (name[0] == '\0').
Playlist findPlaylist(Playlist **head_playlist, char name[]){
    Playlist *current = *head_playlist;

    while(current != NULL && strcmp(name, current->name) != 0){
        current = current->next;
    }

    if(current == NULL){
        puts("Playlist no encontrada.");
        Playlist not_found = {0};
        return not_found;
    } else {
        return *current;
    }
}

// Elimina todas las canciones de la playlist (la playlist se conserva vacia).
void cleanPlaylist(Playlist **head_playlist, char name[]){
    Playlist *current = *head_playlist;

    while(current != NULL && strcmp(name, current->name) != 0){
        current = current->next;
    }

    if(current == NULL){
        puts("Playlist no encontrada.");
        return;
    } else {
        current->total_songs = 0;
        Song *current_song = current->head;
        Song *song = NULL;
        while(current_song != NULL){
            song = current_song->next;
            free(current_song);
            current_song = song;
        }
        current->head = NULL;
        current->current = NULL;
        puts("Playlist vaciada correctamente");
    }
}

// ===================== UTILIDADES DE ENTRADA Y BUSQUEDA =====================

// Muestra un mensaje y lee una linea completa desde teclado (sin el '\n').
// Si se cierra la entrada (EOF), termina el programa.
static void readLine(const char *prompt, char *buf, int size){
    printf("%s", prompt);
    fflush(stdout);
    if(fgets(buf, size, stdin) == NULL){
        puts("");
        exit(0);
    }
    buf[strcspn(buf, "\n")] = '\0';
}

// Lee un entero desde teclado. Repite la pregunta hasta recibir un numero valido.
static int readInt(const char *prompt){
    char buf[64];
    char *end;
    long value;

    while(1){
        readLine(prompt, buf, sizeof(buf));
        value = strtol(buf, &end, 10);
        if(end != buf && *end == '\0')
            return (int)value;
        puts("Entrada invalida. Ingrese un numero.");
    }
}

// Busca una playlist por nombre y retorna su puntero real (no una copia),
// necesario para poder modificar sus canciones. Retorna NULL si no existe.
static Playlist *getPlaylist(Playlist *head, char name[]){
    Playlist *current = head;
    while(current != NULL && strcmp(current->name, name) != 0)
        current = current->next;
    return current;
}

// Imprime todas las playlists con su numero de canciones.
static void listPlaylists(Playlist *head){
    if(head == NULL){
        puts("No hay playlists registradas.");
        return;
    }

    int i = 1;
    for(Playlist *p = head; p != NULL; p = p->next, i++)
        printf("%d. %s (%d canciones)\n", i, p->name, p->total_songs);
}

// Imprime las canciones de una playlist en formato de tabla.
// La duracion se muestra en formato minutos:segundos.
static void listSongs(Playlist *playlist){
    if(playlist->head == NULL){
        puts("La playlist no tiene canciones.");
        return;
    }

    printf("\n%-3s %-30s %-25s %s\n", "#", "Titulo", "Artista", "Duracion");
    int i = 1;
    for(Song *s = playlist->head; s != NULL; s = s->next, i++)
        printf("%-3d %-30s %-25s %d:%02d\n",
               i, s->title, s->artist, s->duration / 60, s->duration % 60);
}

// ===================== OPCIONES DEL MENU DE PLAYLISTS =====================

// Opcion 1: pide un nombre y crea una playlist nueva (sin nombres repetidos).
static void optCreatePlaylist(Playlist **head){
    char name[50];
    readLine("Nombre de la nueva playlist: ", name, sizeof(name));

    if(name[0] == '\0'){
        puts("El nombre no puede estar vacio.");
        return;
    }
    if(getPlaylist(*head, name) != NULL){
        puts("Ya existe una playlist con ese nombre.");
        return;
    }

    addPlaylist(head, name);
    puts("Playlist creada correctamente.");
}

// Opcion 3: busca una playlist por nombre y muestra sus datos.
static void optFindPlaylist(Playlist **head){
    char name[50];
    readLine("Nombre de la playlist a buscar: ", name, sizeof(name));

    Playlist found = findPlaylist(head, name);
    if(found.name[0] != '\0')
        printf("Nombre: %s | Canciones: %d\n", found.name, found.total_songs);
}

// Opcion 4: cambia el nombre de una playlist.
static void optRenamePlaylist(Playlist **head){
    char old_name[50];
    char new_name[50];
    readLine("Nombre actual de la playlist: ", old_name, sizeof(old_name));
    readLine("Nuevo nombre: ", new_name, sizeof(new_name));

    if(new_name[0] == '\0'){
        puts("El nuevo nombre no puede estar vacio.");
        return;
    }
    updatePlaylist(head, old_name, new_name);
}

// Opcion 5: elimina todas las canciones de una playlist.
static void optCleanPlaylist(Playlist **head){
    char name[50];
    readLine("Nombre de la playlist a vaciar: ", name, sizeof(name));
    cleanPlaylist(head, name);
}

// Opcion 6: elimina una playlist completa (con sus canciones).
static void optDeletePlaylist(Playlist **head){
    char name[50];
    readLine("Nombre de la playlist a eliminar: ", name, sizeof(name));
    deletePlaylist(head, name);
}

// ===================== OPCIONES DEL MENU DE CANCIONES =====================

// Opcion 1 del submenu: agrega una cancion a la playlist.
static void optAddSong(Playlist *playlist){
    char title[50];
    char artist[50];
    readLine("Titulo: ", title, sizeof(title));
    readLine("Artista: ", artist, sizeof(artist));
    int duration = readInt("Duracion (segundos): ");

    if(title[0] == '\0'){
        puts("El titulo no puede estar vacio.");
        return;
    }
    if(duration < 0){
        puts("La duracion no puede ser negativa.");
        return;
    }

    addSong(playlist, title, artist, duration);
    puts("Cancion agregada correctamente.");
}

// Opcion 3 del submenu: busca una cancion por titulo y muestra sus datos.
static void optFindSong(Playlist *playlist){
    char title[50];
    readLine("Titulo de la cancion a buscar: ", title, sizeof(title));

    Song found = findSong(playlist, title);
    if(found.title[0] != '\0')
        printf("Titulo: %s | Artista: %s | Duracion: %d:%02d\n",
               found.title, found.artist, found.duration / 60, found.duration % 60);
}

// Opcion 4 del submenu: cambia la duracion de una cancion.
static void optUpdateSong(Playlist *playlist){
    char title[50];
    readLine("Titulo de la cancion a actualizar: ", title, sizeof(title));
    int duration = readInt("Nueva duracion (segundos): ");

    if(duration < 0){
        puts("La duracion no puede ser negativa.");
        return;
    }
    updateSong(playlist, title, duration);
}

// Opcion 5 del submenu: elimina una cancion de la playlist.
static void optDeleteSong(Playlist *playlist){
    char title[50];
    readLine("Titulo de la cancion a eliminar: ", title, sizeof(title));
    deleteSong(playlist, title);
}

// Submenu de canciones: pide el nombre de una playlist y permite gestionar sus canciones.
// Opcion 0 regresa al menu principal.
static void menuSongs(Playlist *head){
    char name[50];
    readLine("Nombre de la playlist: ", name, sizeof(name));

    Playlist *playlist = getPlaylist(head, name);
    if(playlist == NULL){
        puts("Playlist no encontrada.");
        return;
    }

    int option;
    do {
        printf("\n---------- CANCIONES DE \"%s\" ----------\n", playlist->name);
        puts("1. Agregar cancion");
        puts("2. Listar canciones");
        puts("3. Buscar cancion");
        puts("4. Actualizar duracion de una cancion");
        puts("5. Eliminar cancion");
        puts("0. Volver al menu principal");
        puts("-----------------------------------------");

        option = readInt("Seleccione una opcion: ");

        switch(option){
            case 1: optAddSong(playlist);    break;
            case 2: listSongs(playlist);     break;
            case 3: optFindSong(playlist);   break;
            case 4: optUpdateSong(playlist); break;
            case 5: optDeleteSong(playlist); break;
            case 0: break;
            default: puts("Opcion no valida.");
        }
    } while(option != 0);
}

// ===================== MENU PRINCIPAL Y PROGRAMA =====================

// Muestra el menu principal.
static void showMainMenu(void){
    puts("\n=========== GESTOR DE PLAYLISTS ===========");
    puts(" 1. Crear playlist");
    puts(" 2. Listar playlists");
    puts(" 3. Buscar playlist");
    puts(" 4. Renombrar playlist");
    puts(" 5. Vaciar playlist");
    puts(" 6. Eliminar playlist");
    puts(" 7. Gestionar canciones de una playlist");
    puts(" 0. Salir");
    puts("===========================================");
}

// Libera toda la memoria: canciones de cada playlist y las playlists.
static void freeAll(Playlist *head){
    while(head != NULL){
        Playlist *next = head->next;

        Song *song = head->head;
        while(song != NULL){
            Song *next_song = song->next;
            free(song);
            song = next_song;
        }

        free(head);
        head = next;
    }
}

// Punto de entrada: ejecuta el ciclo del menu principal hasta elegir 0 (Salir).
int main(void){
    Playlist *head_playlist = NULL;
    int option;

    do {
        showMainMenu();
        option = readInt("Seleccione una opcion: ");

        switch(option){
            case 1: optCreatePlaylist(&head_playlist);  break;
            case 2: listPlaylists(head_playlist);       break;
            case 3: optFindPlaylist(&head_playlist);    break;
            case 4: optRenamePlaylist(&head_playlist);  break;
            case 5: optCleanPlaylist(&head_playlist);   break;
            case 6: optDeletePlaylist(&head_playlist);  break;
            case 7: menuSongs(head_playlist);           break;
            case 0: puts("Saliendo del programa...");   break;
            default: puts("Opcion no valida.");
        }
    } while(option != 0);

    freeAll(head_playlist);
    return 0;
}
