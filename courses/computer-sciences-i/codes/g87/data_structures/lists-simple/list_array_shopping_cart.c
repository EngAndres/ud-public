/*
This file has a simple implementation of a shopping cart using an 
array as the underlying data structure. 

It includes basic operations such as insertion, deletion, search, 
and update of products in the cart. 

The shopping cart can hold up to 10 products, and each product has 
a name, price, code, and quantity. The program also provides a 
menu-driven interface for users to interact with the shopping cart.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

/* ADJUSTMENTS:
1. Always make malloc for all the char*
2. list_init must receive ShoppingCart* (pointer), not ShoppingCart by value;
   otherwise the initialisation only affects a local copy and the caller's
   array remains uninitialised (garbage, non-NULL elements).
3. In new_product, malloc(strlen(new_name)) was missing +1 for the null
   terminator, and the result was immediately overwritten with p->name = new_name
   (memory leak, no copy). Fixed with malloc(strlen+1) + strcpy.
4. private_lineal_search_by_name used == to compare char* (pointer comparison),
   which always fails for different buffers. Fixed with strcmp(...) == 0.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *name;
    double price;
    int code;
    int quantity;
} Product;

typedef struct {
    Product *products[10];
    int items;
} ShoppingCart;


// Basic Functions
static Product *new_product(char *new_name, double new_price, int new_code, int new_quantity) {
    Product *p = malloc(sizeof(Product));
    if(!p){
        perror("Malloc Failed.");
        exit(EXIT_FAILURE);
    }
    p->name = malloc(strlen(new_name) + 1);
    strcpy(p->name, new_name);
    p->code = new_code;
    p->price = new_price;
    p->quantity = new_quantity;
    return p;
}

void list_init(ShoppingCart *list) {
    for(int i = 0; i < 10; i++)
        list->products[i] = NULL;
    list->items = 0;
}

/// Insertions
void insert(ShoppingCart *list, Product *product){
    int index = 0;
    while(index < 10 && list->products[index]){
        index++;
    }
    if(index < 10){
        list->products[index] = product;
        list->items++;
    } else {
        puts("Shopping cart is full.");
    }
}

// Search
int private_lineal_search_by_name(const ShoppingCart *list, char* name){
    int index = 0;
    while(index < 10 && list->products[index]){
        if(strcmp(list->products[index]->name, name) == 0)
            return index;
        
        index++;
    }
    return -1;
}

//Update
void update_quantity(ShoppingCart *cart, char *name, int quantity){
    if(quantity < 1){
        puts("Quantity should be 1 or greater.");
        return;
    }
    int index = private_lineal_search_by_name(cart, name);
    if(index != -1){
        cart->products[index]->quantity = quantity;
    } else {
        fprintf(stderr, "Product with name %s is not in the cart.", name);
    }
}

// Deletions
void delete_by_name(ShoppingCart *list, char *name){
    int index = private_lineal_search_by_name(list, name);
    
    if(index == -1){ //Empty list
        fprintf(stderr, "delete: name %s not fount in the list.", name);
        return;
    } 

    for(int i = index; i < 10 - 1; i++){
        list->products[i] = list->products[i + 1];
        if(!list->products[i])
            break;
    }
    list->products[9] = NULL;
    list->items--;
}

// Utilities
void display_cart(const ShoppingCart *cart){
    if(!cart->products[0]){
        puts("Shopping Cart is empty");
        return;
    }

    printf("\tHEAD\n");
    int index = 0;
    while(cart->products[index]){
        Product *temp = cart->products[index];
        printf("Code: %d\tName: %s\tPrice: %.2f\tQuantity: %d\n", 
            temp->code, temp->name, temp->price, temp->quantity);
        index++;
    }
    printf("\tTAIL.\n");
    printf("Size: %d\n\n", cart->items);
}

int get_item_count(ShoppingCart *cart){
    return cart->items;
}

double get_total_price(ShoppingCart *cart){
    double total = 0;
    int index = 0;
    while(index < 10 && cart->products[index]){
        total = total + cart->products[index]->price;
        index++;
    }
    return total;
}

void print_menu(){
    printf("\n\n\t\tMENU\n");
    printf("1. Add Item\n");
    printf("2. Remove Item\n");
    printf("3. Update Quantity\n");
    printf("4. Get Total Price\n");
    printf("5. Get Item Count\n");
    printf("6. Display Cart\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

Product *option_insert(){
    char *name = malloc(50);
    double price;
    int code;
    int quantity;

    printf("\nAdd the product name: ");
    scanf("%99s", name);
    printf("Add the product price: ");
    scanf("%lf", &price);
    printf("Add the product code: ");
    scanf("%d", &code);
    printf("Add the product quantity: ");
    scanf("%d", &quantity);
    return new_product(name, price, code, quantity);
}

void update_option(ShoppingCart *cart){
    char *name = malloc(50);
    int quantity;
    printf("\nProvide the product name: ");
    scanf("%s", name);
    printf("\nAdd the product new quantity: ");
    scanf("%d", &quantity);
    update_quantity(cart, name, quantity);
}

int main(void){

    ShoppingCart cart;
    list_init(&cart);
    int option;

    double price; 
    int items;
    char *name = malloc(50);
    Product *product;
                
                
    do {
        print_menu();
        scanf("%d", &option);

        switch(option){
            case 1:
                product = option_insert();
                printf("%d %s", product->code, product->name);
                insert(&cart, product);
                break;
            case 2:
                printf("\nProvide the product name to be deleted: ");
                scanf("%s", name);
                delete_by_name(&cart, name);
                break;
            case 3:
                update_option(&cart);
                break;
            case 4:
                price = get_total_price(&cart);
                printf("The current price of all the items in the shopping cart is %.2f.\n", price);
                break;
            case 5:
                items = get_item_count(&cart);
                printf("The shooping cart has %d items.\n", items);
                break;
            case 6:
                display_cart(&cart);
                break;
            case 0:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid option.\n");
        }


    } while(option != 0);

    return 0;
}