/**
 * This is a simple implementation of the linear search algorithm in C.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

/**
 * Performs a linear search on an array.
 * 
 * @param data The array to search.
 * @param size The size of the array.
 * @param target The value to search for.
 * @return The index of the target if found, otherwise -1.
 */
int sequencialSearch(int data[], int size, int target){
    for(int i = 0; i < size; i++){
        if(data[i] == target)
            return i; // found it
    }
    return -1; // not found
}

// Main function to demonstrate the linear search algorithm
int main(){
    int data[] = {1, 4, 7, 2, 3, 9, 8};
    int size = 6;
    int target = 3;

    printf("El resultado es: %d", sequencialSearch(data, size, target));
    return 0;
}