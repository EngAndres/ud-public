/**
 * @file hashing.c
 * @brief Simple hashing implementation with chaining.
 *
 * This file provides a basic implementation of a hash table with chaining
 * to handle collisions. It includes functions for initialization, insertion,
 * searching, and printing the hash table.
 *
 * @author Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

#include <stdio.h>

#define SLOTS 10
#define CHAIN_SIZE 5

// Hash table implemented as a 2D array for chaining.
int hashTable[SLOTS][CHAIN_SIZE];

/**
 * @brief Initializes the hash table by setting all entries to -1.
 *
 * This function iterates through the hash table and initializes each slot
 * to -1, indicating that it is empty.
 */
void init() {
    for (int i = 0; i < SLOTS; i++) {
        for (int j = 0; j < CHAIN_SIZE; j++) {
            hashTable[i][j] = -1;
        }
    }
}

/**
 * @brief Computes the hash slot for a given key.
 *
 * This function uses the modulo operator to determine the slot for a given
 * key. This can be replaced with other hash functions.
 *
 * @param key The key to hash.
 * @return The calculated slot in the hash table.
 */
int hash_function(int key) {
    // Simple modulo-based hash function.
    return key % SLOTS;
}

/**
 * @brief Inserts a key into the hash table.
 *
 * This function calculates the slot for the key and inserts it into the
 * first available position in the chain for that slot.
 *
 * @param key The key to insert.
 */
void insert(int key) {
    int slot = hash_function(key);
    for (int j = 0; j < CHAIN_SIZE; j++) {
        if (hashTable[slot][j] == -1) {
            hashTable[slot][j] = key;
            return; // Exit after insertion.
        }
    }
    // This basic implementation does not handle chain overflow.
}

/**
 * @brief Searches for a key in the hash table.
 *
 * This function finds the slot for the key and then searches the chain
 * at that slot to find the key.
 *
 * @param key The key to search for.
 * @return The slot index if the key is found; otherwise, -1.
 */
int search(int key) {
    int slot = hash_function(key);
    for (int j = 0; j < CHAIN_SIZE; j++) {
        // If we hit an empty spot, the key is not in the table.
        if (hashTable[slot][j] == -1) {
            return -1;
        }
        // If the key is found, return the slot index.
        if (hashTable[slot][j] == key) {
            return slot;
        }
    }
    // Return -1 if the key is not found after checking the whole chain.
    return -1;
}

/**
 * @brief Prints the contents of the hash table.
 *
 * This function iterates through each slot and chain in the hash table
 * and prints its contents.
 */
void printTable() {
    for (int i = 0; i < SLOTS; i++) {
        printf("SLOT [%d]: ", i);
        for (int j = 0; j < CHAIN_SIZE; j++) {
            printf(" %d ", hashTable[i][j]);
        }
        printf("\n");
    }
}

/**
 * @brief Main function to demonstrate the hashing implementation.
 *
 * Initializes the hash table, inserts some values, prints the table,
 * and performs a search for a key.
 *
 * @return 0 on successful execution.
 */
int main() {
    init();
    insert(234);
    insert(543);
    insert(2);
    insert(456);
    insert(123);
    insert(876);
    insert(1);
    printTable();

    int key_to_search = 123;
    int search_result = search(key_to_search);

    if (search_result != -1) {
        printf("\nSearch for %d found in slot: %d\n", key_to_search, search_result);
    } else {
        printf("\nSearch for %d not found.\n", key_to_search);
    }

    key_to_search = 999;
    search_result = search(key_to_search);

    if (search_result != -1) {
        printf("Search for %d found in slot: %d\n", key_to_search, search_result);
    } else {
        printf("Search for %d not found.\n", key_to_search);
    }

    return 0;
}
