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
void init_cart(ShoppingCart *cart) {
    cart->count = 0;
}

int find_item(ShoppingCart *cart, char *name){
    for(int i = 0; i < cart->count; i++){
        if(strcmp(name, cart->items[i].item.name) == 0) {
            // they are equal
            return i;
        }
    }
    return -1;
}

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















