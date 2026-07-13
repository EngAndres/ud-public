/**
 * @file linear_search.c
 * @brief Implementation of the linear search algorithm.
 *
 * This file contains a simple implementation of the linear search algorithm
 * for finding a target value in an integer array.
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

/**
 * @brief Performs a linear search on an array to find a target value.
 *
 * This function iterates through each element of the array sequentially
 * to find the index of the target value.
 *
 * @param data The integer array to search.
 * @param size The number of elements in the array.
 * @param target The value to search for.
 * @return The index of the target if found; otherwise, -1.
 */
int sequentialSearch(int data[], int size, int target) {
    // Iterate through the array from the beginning.
    for (int i = 0; i < size; i++) {
        // If the current element matches the target, return its index.
        if (data[i] == target) {
            return i; // Target found.
        }
    }
    // Return -1 if the target is not found after checking all elements.
    return -1; // Target not found.
}

/**
 * @brief Main function to demonstrate the linear search algorithm.
 *
 * Initializes an array and demonstrates the use of the sequentialSearch
 * function to find a target value.
 *
 * @return 0 on successful execution.
 */
int main() {
    int data[] = {1, 4, 7, 2, 3, 9, 8};
    int size = sizeof(data) / sizeof(data[0]);
    int target = 3;

    int result = sequentialSearch(data, size, target);

    if (result != -1) {
        printf("Target %d found at index: %d\n", target, result);
    } else {
        printf("Target %d not found in the array.\n", target);
    }

    return 0;
}