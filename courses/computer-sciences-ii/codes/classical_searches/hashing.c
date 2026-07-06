#include <stdio.h>

#define SLOTS 10

int hashTable[SLOTS][5];

void init(){
    for(int i = 0; i < SLOTS; i++)
    for(int j = 0; j < 5; j++)    
        hashTable[i][j] = -1;
}

int hash_function(int key){
    int slot = key % SLOTS; // change this line for another function
    return slot;
}

void insert(int key){
    int slot = hash_function(key);
    for(int j = 0; j < 5; j++)
        if(hashTable[slot][j] == -1){
            hashTable[slot][j] = key;
            break;
        }
}

int search(int key){
    int slot = hash_function(key);
    for(int j = 0; j < 5; j++){
        if(hashTable[slot][j] == -1)
            return -1;
        else
            if(hashTable[slot][j] == key)
                return slot;
    }
    
}

void printTable(){
    for(int i = 0; i < SLOTS; i++){
        printf("SLOT [%d]: ", i);
        for(int j = 0; j < 5; j++){ 
            printf(" %d ", hashTable[i][j]);
        }
        puts("\n");
    }
}

int main(){
    init();
    insert(234);
    insert(543);
    insert(2);
    insert(456);
    insert(123);
    insert(876);
    insert(1);
    printTable();
    int key = 1233;
    printf("\n\nSearch for %d is: %d", key, search(key));
    return 0;
}
