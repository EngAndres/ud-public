/**
 * @file single_residue.c
 * @brief Simple hashing with single residue and collision detection.
 *
 * This file demonstrates a basic hashing technique using a single residue
 * (modulo) function. It detects but does not resolve collisions.
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

#define SLOTS 7

// Memory array to store hashed values.
int memory[SLOTS];

/**
 * @brief Initializes the memory array by setting all entries to -1.
 *
 * This function iterates through the memory array and initializes each slot
 * to -1, indicating that it is empty.
 */
void init() {
    for (int i = 0; i < SLOTS; i++) {
        memory[i] = -1;
    }
}

/**
 * @brief Stores values in the memory array using single residue hashing.
 *
 * This function attempts to place each value in a slot determined by the
 * modulo operator. If a collision occurs (the slot is already occupied),
 * it prints a collision message.
 *
 * @param values An array of integer values to be stored.
 * @param size The number of elements in the values array.
 */
void residue_store(int values[], int size) {
    for (int i = 0; i < size; i++) {
        // Hash function to determine the slot.
        int slot = values[i] % SLOTS;

        // If the slot is empty, place the value there.
        if (memory[slot] == -1) {
            memory[slot] = values[i];
        } else {
            // If the slot is occupied, report a collision.
            printf("COLLISION!!! Slot %d is already taken by %d. Cannot store %d.\n", slot, memory[slot], values[i]);
        }
    }
}

/**
 * @brief Prints the contents of the memory array.
 *
 * This function iterates through the memory array and prints the value
 * stored in each slot.
 */
void printMemory() {
    printf("\nMemory contents:\n");
    for (int i = 0; i < SLOTS; i++) {
        printf("Slot: %d -> %d\n", i, memory[i]);
    }
}

/**
 * @brief Main function to demonstrate single residue hashing.
 *
 * Initializes the memory, stores a set of test values that will cause
 * a collision, and prints the final state of the memory.
 *
 * @return 0 on successful execution.
 */
int main() {
    // Test data where 12 and 19 will hash to the same slot (5).
    int test[] = {12, 27, 42, 19};
    int sizeExample = sizeof(test) / sizeof(test[0]);

    init();
    residue_store(test, sizeExample);
    printMemory();

    return 0;
}