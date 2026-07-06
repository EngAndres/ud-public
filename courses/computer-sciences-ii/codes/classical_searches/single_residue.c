#include <stdio.h>

#define SLOTS 7
int memory[SLOTS];

void init(){
    for(int i = 0; i < SLOTS; i++)
        memory[i] = -1;
}

void residue_store(int values[], int size){
    for(int i = 0; i < size; i++){
        int slot = values[i] % SLOTS;
        if(memory[slot] == -1)
            memory[slot] = values[i];
        else
            printf("COLLISION!!!");
    }
}

void printMemory(){
    for(int i = 0; i < SLOTS; i++)
        printf("Slot: %d -> %d\t", i, memory[i]);
}

int main(){
    int test[] = {12, 27, 42};
    int sizeExaxmple = 3;
    init();
    residue_store(test, sizeExaxmple);
    printMemory();
    return 0;
}