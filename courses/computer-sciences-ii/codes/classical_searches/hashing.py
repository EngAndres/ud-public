"""This module provides a simple implementation of a hash table with chaining.

It includes several hash functions and basic operations like insert and search.
"""

from typing import Dict, List, Tuple

# Define the number of slots in the hash table.
SLOTS: int = 10

# The hash table is represented as a dictionary where keys are slots
# and values are lists of keys that hash to that slot.
hash_table: Dict[int, List[int]] = {}


def hash_function_module(key: int) -> int:
    """Computes the hash slot for a given key using the modulo operator.

    Args:
        key: The integer key to hash.

    Returns:
        The calculated slot in the hash table.
    """
    return key % SLOTS


def hash_function_midsquare(key: int) -> int:
    """Computes the hash slot using the mid-square method.

    This method squares the key and extracts the middle digits.

    Args:
        key: The integer key to hash.

    Returns:
        The calculated slot as an integer.
    """
    squared = str(key**2)
    # Determine how many digits to remove from each side.
    remove_digits = len(squared) // 4
    if remove_digits == 0 and len(squared) > 1:
        remove_digits = 1
    
    # Extract the middle part of the squared number.
    if len(squared) > 2 * remove_digits:
        slot_str = squared[remove_digits:-remove_digits]
    else:
        slot_str = squared

    return int(slot_str) % SLOTS


def hash_function_truncate(key: int) -> int:
    """Computes the hash slot by truncating the key.

    This method extracts digits from specific positions in the key's string
    representation to form the slot.

    Args:
        key: The integer key to hash.

    Returns:
        The calculated slot as an integer.
    """
    positions = (0, 2, 4)  # Example positions to extract.
    key_str = str(key)
    slot_str = ""
    for p in positions:
        if p < len(key_str):
            slot_str += key_str[p]

    if not slot_str:
        return 0

    return int(slot_str) % SLOTS


def insert(key: int):
    """Inserts a key into the hash table.

    This function calculates the slot for the key and appends the key to the
    list at that slot (chaining).

    Args:
        key: The integer key to insert.
    """
    slot = hash_function_module(key)
    if slot not in hash_table:
        hash_table[slot] = []
    hash_table[slot].append(key)


def search(key: int) -> Tuple[int, int] | None:
    """Searches for a key in the hash table.

    This function finds the slot for the key and then searches the list
    at that slot to find the key.

    Args:
        key: The integer key to search for.

    Returns:
        A tuple containing the slot and the index in the chain if the key is
        found, otherwise None.
    """
    slot = hash_function_module(key)
    if slot in hash_table:
        for i, key_i in enumerate(hash_table[slot]):
            if key_i == key:
                return (slot, i)
    return None

# Example usage:
if __name__ == "__main__":
    # Insert some keys into the hash table.
    keys_to_insert = [234, 543, 2, 456, 123, 876, 1]
    for k in keys_to_insert:
        insert(k)

    # Print the hash table.
    print("Hash Table:")
    for slot, values in sorted(hash_table.items()):
        print(f"SLOT [{slot}]: {values}")

    # Search for a key.
    key_to_search = 123
    result = search(key_to_search)
    if result:
        print(f"\nSearch for {key_to_search} found at slot {result[0]}, index {result[1]}.")
    else:
        print(f"\nSearch for {key_to_search} not found.")

    key_to_search = 999
    result = search(key_to_search)
    if result:
        print(f"Search for {key_to_search} found at slot {result[0]}, index {result[1]}.")
    else:
        print(f"Search for {key_to_search} not found.")