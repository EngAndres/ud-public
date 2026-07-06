/**
 * This is a simple implementation of the binary search algorithm in C.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

/**
 * Performs a binary search on a sorted array.
 * 
 * @param sortedData The sorted array to search.
 * @param size The size of the array.
 * @param target The value to search for.
 * @return The index of the target if found, otherwise -1.
 */
int binarySearch(int sortedData[], int size, int target){
    int lower = 0;
    int upper = size - 1;

    while(lower <= upper){
        int middle = (int)((lower + upper) / 2);
        if(sortedData[middle] == target)
            return middle; // found it
        
        if(target < sortedData[middle]) // discart higher half
            upper = middle - 1;
        else
            lower = middle + 1;    
    }
    return -1; //not found
}

// Main function to demonstrate the binary search algorithm
int main(){
    int data[] = {1, 2, 4, 5, 8, 9, 18};
    int size = 7;
    int target = 9;

    printf("El resultado es: %d", binarySearch(data, size, target));
    return 0;
}