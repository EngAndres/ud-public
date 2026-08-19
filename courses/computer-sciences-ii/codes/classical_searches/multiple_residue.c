/**
 * @file multiple_residue.c
 * @brief Hashing with multiple residue for collision handling.
 *
 * This file demonstrates a hashing technique where collisions are handled
 * by using a secondary hash function (multiple residue method).
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

#define SLOTS 7
#define OPTION 5 // Secondary divisor for collision handling.

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
 * @brief Stores values in the memory array using multiple residue hashing.
 *
 * This function attempts to place each value in a slot determined by a primary
 * hash function (modulo SLOTS). If a collision occurs, it uses a secondary
 * hash function (modulo OPTION) to find an alternative slot.
 *
 * @param values An array of integer values to be stored.
 * @param size The number of elements in the values array.
 */
void residue_store(int values[], int size) {
    for (int i = 0; i < size; i++) {
        // Primary hash function to determine the initial slot.
        int slot = values[i] % SLOTS;

        // If the primary slot is empty, place the value there.
        if (memory[slot] == -1) {
            memory[slot] = values[i];
        } else {
            // If a collision occurs, use a secondary hash function.
            printf("Collision at slot %d for value %d. Trying secondary hash.\n", slot, values[i]);
            int slot_option = values[i] % OPTION;

            // Check if the secondary slot is within the bounds of the memory array.
            if (slot_option < SLOTS && memory[slot_option] == -1) {
                memory[slot_option] = values[i];
            } else {
                // If the secondary slot is also occupied or out of bounds, report a collision.
                printf("COLLISION!!! Both primary and secondary slots are occupied for value %d.\n", values[i]);
            }
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
 * @brief Main function to demonstrate the multiple residue hashing.
 *
 * Initializes the memory, stores a set of test values, and prints the
 * final state of the memory.
 *
 * @return 0 on successful execution.
 */
int main() {
    int test[] = {12, 27, 42, 19}; // Added a value that will use the secondary hash.
    int sizeExample = sizeof(test) / sizeof(test[0]);

    init();
    residue_store(test, sizeExample);
    printMemory();

    return 0;
}