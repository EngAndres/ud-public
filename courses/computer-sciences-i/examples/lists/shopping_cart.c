/*
 * shopping_cart.c
 *
 * Example of a shopping cart implemented with a fixed-size array of items.
 * Supports adding, removing and updating the quantity of items.
 */

// Libraries - Dependencies
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Constants 
#define MAX_ITEMS 10
#define NAME_MAX_LENGTH 50
#define DESC_MAX_LENGTH 100

// My own datatypes
typedef struct {
    char name[NAME_MAX_LENGTH];
    double price;
    char description[DESC_MAX_LENGTH];
} Item;

typedef struct {
    Item item;
    int quantity;
} CartItem;

typedef struct {
    CartItem items[MAX_ITEMS];
    int count;
} ShoppingCart;

// Operations
/* 
* is used to access to a variable using the pointer, it means
directly to the memory allocation 
*/
/*
 * Initializes the cart as empty.
 *
 * cart: pointer to the cart to initialize.
 */
void init_cart(ShoppingCart *cart) {
    cart->count = 0;
}

/*
 * Searches the cart for an item with the given name.
 *
 * cart: pointer to the cart to search.
 * name: name of the item to find.
 * 
 * Returns the index of the item in the cart, or -1 if it is not found.
 */
int find_item(ShoppingCart *cart, char *name){
    for(int i = 0; i < cart->count; i++){
        if(strcmp(name, cart->items[i].item.name) == 0) {
            // they are equal
            return i;
        }
    }
    return -1;
}

/*
 * Adds an item to the cart. If an item with the same name already exists,
 * its quantity is increased instead.
 *
 * cart: pointer to the cart.
 * item: item to add.
 * quantity: number of units to add (must be positive).
 * 
 * Returns true if the item was added, false otherwise (invalid quantity or full cart).
 */
bool add_item(ShoppingCart *cart, Item item, int quantity){
    if(quantity <= 0){
        puts("La cantidad del articulo no puede ser negativa.\n");
        return false;
    }

    if(cart->count == MAX_ITEMS){
        puts("El carrito ya se encuentra lleno.\n");
        return false;
    }

    int index_item = find_item(cart, item.name);
    if(index_item != -1){ // Item yet exists
        cart->items[index_item].quantity += quantity;
        return true;
    }

    cart->items[cart->count].item = item;
    cart->items[cart->count].quantity = quantity;
    cart->count++;
    return true;
}

/*
 * Removes an item from the cart by name, shifting the following items left.
 *
 * cart: pointer to the cart.
 * name: name of the item to remove.
 * 
 * Returns true if the item was removed, false if it does not exist.
 */
bool remove_item(ShoppingCart *cart, const char *name) {
    int index = find_item(cart, name);
    
    if (index == -1){
        puts("No se puede borrar porque no existe un elemento con el nombre proporcionado.");
        return false;
    }

    for(int i = index; i < cart->count; i++) 
        cart->items[i] = cart->items[i + 1];
    cart->count--;
    return true;
}

/*
 * Replaces the quantity of an existing item in the cart.
 *
 * cart: pointer to the cart.
 * name: name of the item to update.
 * new_quantity: new quantity (must be positive).
 * 
 * Returns true if the quantity was updated, false otherwise.
 */
bool update_quantity(ShoppingCart *cart, const char *name, int new_quantity){
    if(new_quantity <= 0){
        puts("La cantidad a actualizar debe ser un número positivo.");
        return false;
    }

    int index = find_item(cart, name);
    if (index == -1){
        puts("No se puede actualizar porque no existe un elemento con el nombre proporcionado.");
        return false;
    }

    cart->items[index].quantity = new_quantity;
    return true;
}


double get_total_price(ShoppingCart *cart){
    double total = 0.0;
    for(int i = 0; i < cart->count; i++)
        total += (cart->items[i].quantity * cart->items[i].item.price);
    return total;
}


bool is_empty(ShoppingCart *cart){
    return cart->count == 0;
}


void display_cart(ShoppingCart *cart){
    if(is_empty(cart)){
        puts("El carrito está vacío.\n");
        return;
    }

    printf("\n%-50s %8s %10s %10s\n", "Nombre", "Precio", "Cantidad", "Subtotal");
    printf("---------------------------------------------------------------------");
    for(int i = 0; i < cart->count; i++){
        CartItem *cart_item = &cart->items[i];
        printf("\n%-50s %8.2f %10d %10.2f\n", cart_item->item.name, cart_item->item.price, 
            cart_item->quantity, (cart_item->quantity * cart_item->item.price));
    }
    printf("---------------------------------------------------------------------");
    printf("Total: $%.3f", get_total_price(cart));
}

