/*
This file has a simple implementation of a shopping cart using an
array as the underlying data structure.

It includes basic operations such as insertion, deletion by name,
search by name, updating product quantity, getting the item count,
computing the total price, and displaying the cart contents.

The shopping cart can hold up to 10 products, and each product has
a name, quantity, and price. The program also provides a
menu-driven interface for users to interact with the shopping cart.

Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
*/

/* ADJUSTMENTS:
1. In new_product, name was assigned by pointer without copying the
   string data. Fixed with malloc(strlen+1) + strcpy.
2. linear_search_by_name used == for string comparison (pointer
   equality). Fixed with strcmp(...) == 0.
3. update_quantity: print() -> printf(); typo "updaet" corrected.
4. display_cart: format specifier %d -> %s for the name field.
5. main: ShoppingCart declared as an uninitialised pointer. Fixed to
   a stack variable with its address passed to init_list.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int quantity;
    double price;
    char *name;
} Product;

typedef struct {
    Product *products[10];
    int items;
} ShoppingCart;


static Product *new_product(char *new_name, int new_quantity, double new_price) {
    Product *p = malloc(sizeof(Product));
    if (!p) {
        perror("Malloc fails.");
        exit(EXIT_FAILURE);
    }
    p->name = malloc(strlen(new_name) + 1);
    strcpy(p->name, new_name);
    p->quantity = new_quantity;
    p->price = new_price;
    return p;
}

void init_list(ShoppingCart *cart) {
    for (int i = 0; i < 10; i++)
        cart->products[i] = NULL;
    cart->items = 0;
}

/* INSERT */
void insert(ShoppingCart *cart, Product *product) {
    int index = 0;
    while (index < 10 && cart->products[index])
        index++;
    if (index < 10) {
        cart->products[index] = product;
        cart->items++;
    } else {
        puts("Shopping cart is full.");
    }
}

int linear_search_by_name(ShoppingCart *cart, char *name_) {
    int index = 0;
    while (index < 10 && cart->products[index]) {
        if (strcmp(cart->products[index]->name, name_) == 0)
            return index;
        index++;
    }
    return -1;
}

/* Delete */
void delete_product(ShoppingCart *cart, char *name) {
    int index = linear_search_by_name(cart, name);
    if (index != -1) {
        free(cart->products[index]->name);
        free(cart->products[index]);
        for (int i = index; i < 9; i++)
            cart->products[i] = cart->products[i + 1];
        cart->products[9] = NULL;
        cart->items--;
    } else {
        printf("No product with name '%s'.\n", name);
    }
}

/* Additionals */
void update_quantity(ShoppingCart *cart, char *name, int new_quantity) {
    if (new_quantity < 1) {
        fprintf(stderr, "Quantity %d is not a valid value.\n", new_quantity);
        return;
    }
    int index = linear_search_by_name(cart, name);
    if (index != -1) {
        cart->products[index]->quantity = new_quantity;
        printf("Successful update.\n");
    } else {
        printf("There is no product with name '%s'.\n", name);
    }
}

int get_items_count(ShoppingCart *cart) {
    return cart->items;
}

double get_total_price(ShoppingCart *cart) {
    double total_price = 0.0;
    int index = 0;
    while (index < 10 && cart->products[index]) {
        total_price += cart->products[index]->price;
        index++;
    }
    return total_price;
}

void display_cart(ShoppingCart *cart) {
    printf("\tSHOPPING CART:\n");
    int index = 0;
    Product *temp;
    while (index < 10 && cart->products[index]) {
        temp = cart->products[index];
        printf("Name: %s\tQuantity: %d\tPrice: %.2f\n",
               temp->name, temp->quantity, temp->price);
        index++;
    }
    printf(" END, size=%d\n", cart->items);
}

void print_menu() {
    printf("\n\n\t\tMENU\n");
    printf("1. Add Product\n");
    printf("2. Remove Product\n");
    printf("3. Update Quantity\n");
    printf("4. Get Total Price\n");
    printf("5. Get Item Count\n");
    printf("6. Display Cart\n");
    printf("0. Exit\n");
    printf("Choose an option: ");
}

int main(void) {
    ShoppingCart cart;
    init_list(&cart);
    int option;
    char name[50];
    int quantity;
    double price;

    do {
        print_menu();
        scanf("%d", &option);

        switch (option) {
            case 1:
                printf("Product name: ");
                scanf(" %49[^\n]", name);
                printf("Quantity: ");
                scanf("%d", &quantity);
                printf("Price: ");
                scanf("%lf", &price);
                insert(&cart, new_product(name, quantity, price));
                break;
            case 2:
                printf("Product name to remove: ");
                scanf(" %49[^\n]", name);
                delete_product(&cart, name);
                break;
            case 3:
                printf("Product name: ");
                scanf(" %49[^\n]", name);
                printf("New quantity: ");
                scanf("%d", &quantity);
                update_quantity(&cart, name, quantity);
                break;
            case 4:
                printf("Total price: $%.2f\n", get_total_price(&cart));
                break;
            case 5:
                printf("Items in cart: %d\n", get_items_count(&cart));
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
    } while (option != 0);

    return 0;
}
