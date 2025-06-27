
import java.util.Scanner;

public class App_2 {
    
    /**
     * This method creates a Pizza object based on user input.
     * It prompts the user for the flavor, size, and days s]
     * \lop00ce preparation,
     * and returns a new Pizza object.
     * 
     * @param scanner
     * @return Pizza
     * @throws Exception
     */
    public static Pizza createPizza(Scanner scanner) throws Exception {
        System.out.print("Add flavor:");
        String flavor = scanner.nextLine();

        System.out.print("Add size:");
        Integer size = Integer.parseInt(scanner.nextLine()); 

        System.out.print("Add how many days since preparation?:");
        Integer days = Integer.parseInt(scanner.nextLine()); 

        return new Pizza(flavor, size, days);
    }

    /**
     * This method creates a Burguer object based on user input.
     * It prompts the user for the weight of the burger and returns a new Burguer object.
     * 
     * @param scanner
     * @return Burguer
     * @throws Exception
     */
    public static Burguer createBurguer(Scanner scanner) throws Exception {
        System.out.print("Add weight:");
        Integer weight = Integer.parseInt(scanner.nextLine()); 

        return new Burguer(weight);
    }

    /**
     * This method creates a Hotdog object based on user input.
     * It prompts the user for the type of sausage and how many days since preparation,
     * and returns a new Hotdog object.
     * 
     * @param scanner
     * @return Hotdog
     */
    public static Hotdog createHotdog(Scanner scanner) throws Exception {
        System.out.print("Add sausage type (American/Choriperro):");
        String sausage = scanner.nextLine(); 

        System.out.print("Add how many days since preparation?:");
        Integer days = Integer.parseInt(scanner.nextLine()); 

        return new Hotdog(sausage, days);
    }

    /**
     * This method prints the main menu of the food store.
     * It displays options for adding products, showing the cart,
     * emptying the cart, and exiting the application.
     */
    public static void printMenu() {
        System.out.println("Choose an option:");
        System.out.println("1. Add Pizza");
        System.out.println("2. Add Burguer");
        System.out.println("3. Add Hotdog");
        System.out.println("4. Show Products in Cart");
        System.out.println("5. Empty Cart");
        System.out.println("6. Exit");
    }
    
    public static void main(String[] args) throws Exception {
        Scanner scanner = new Scanner(System.in);
        ShoopingCart cart = new ShoopingCart();

        System.out.println("===== Welcome to the Food Store! =====");

        do{
            printMenu();
            int option = Integer.parseInt(scanner.nextLine());

            if(option == 1){ // Add pizza
                cart.addProduct( createPizza(scanner) );
                System.out.println("Pizza added to cart.\n\n");
            }
            else if(option == 2){ // Add burguer
                cart.addProduct( createBurguer(scanner) );
                System.out.println("Burguer added to cart.\n\n");
            } 
            else if(option == 3){ // Add hotdog
            
                cart.addProduct( createHotdog(scanner) );
                System.out.println("Hotdog added to cart.\n\n");
            }
            else if(option == 4){ // Show cart
                System.out.println("\nCurrent Shopping Cart:");
                cart.showProducts();
                System.out.println("Total Price: " + cart.getCurrentPrice() + "\n");
            }
            else if(option == 5){ // Empty Cart
                cart.emptyCart();
                System.out.println("Cart now is empty.");
            }
            else if(option == 6){
                System.out.println("Exiting the store. Thank you!");
                break;
            }
        }
        while(true);
    }
}
