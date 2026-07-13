/**
 * @file binary_search.c
 * @brief Implementation of the binary search algorithm.
 *
 * This file contains the implementation of the binary search algorithm
 * for finding a target value in a sorted integer array.
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

/**
 * @brief Performs a binary search on a sorted array to find a target value.
 *
 * This function implements the binary search algorithm. It efficiently finds the
 * index of a target value within a sorted integer array by repeatedly dividing
 * the search interval in half.
 *
 * @param sortedData The sorted integer array to search.
 * @param size The number of elements in the array.
 * @param target The value to search for.
 * @return The index of the target if found; otherwise, -1.
 */
int binarySearch(int sortedData[], int size, int target) {
    int lower = 0;
    int upper = size - 1;

    while (lower <= upper) {
        // Calculate the middle index to divide the search interval.
        int middle = lower + (upper - lower) / 2;

        // If the target is found at the middle, return its index.
        if (sortedData[middle] == target) {
            return middle;
        }

        // If the target is smaller, discard the upper half of the array.
        if (target < sortedData[middle]) {
            upper = middle - 1;
        } else {
            // Otherwise, discard the lower half.
            lower = middle + 1;
        }
    }
    // Return -1 if the target is not found in the array.
    return -1;
}

/**
 * @brief Main function to demonstrate the binary search algorithm.
 *
 * Initializes an array and demonstrates the use of the binarySearch function
 * to find a target value.
 *
 * @return 0 on successful execution.
 */
int main() {
    int data[] = {1, 2, 4, 5, 8, 9, 18};
    int size = sizeof(data) / sizeof(data[0]);
    int target = 9;

    int result = binarySearch(data, size, target);

    if (result != -1) {
        printf("Target %d found at index: %d\n", target, result);
    } else {
        printf("Target %d not found in the array.\n", target);
    }

    return 0;
}