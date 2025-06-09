import ShoopingCart;
import Pizza;
import Burguer;
import Hotdog;
public class App {
    
    public static Pizza createPizza(){
        System.out.println("Add flavor:");
        String flavor = System.in.read();

        System.out.println("Add size:");
        Integer size = Integer.parseInt(System.in.read());

        System.out.println("Add how many days since preparation?:");
        Integer days = Integer.parseInt(System.in.read());

        Pizza newPizza = new Pizza(flavor, size, days);
        return newPizza;
    }

    public static Burguer createBurguer(){
        System.out.println("Add weight:");
        Integer weight = Integer.parseInt(System.in.read()();

        Burguer newBurguer = new Burguer(weight);
        return newBurguer;
    }

    public static Hotdog createHotdog(){
        System.out.println("Add sausage type (American/Choriperro):");
        String sausage = System.in.read();

        System.out.println("Add how many days since preparation?:");
        Integer days = Integer.parseInt(System.in.read());

        Hotdog newHotdog = new Hotdog(sausage, days);
        return newHotdog;
    }

    public static void printMenu() {
        System.out.println("Welcome to the Food Store! Choose an option:");
        System.out.println("1. Add Pizza");
        System.out.println("2. Add Burguer");
        System.out.println("3. Add Hotdog");
        System.out.println("4. Show Products in Cart");
        System.out.println("5. Empty Cart");
        System.out.println("6. Exit");
    }
    
    public static void main(String[] args) throws Exception {
        ShoopingCart cart = new ShoopingCart();

        do{
            printMenu();
            int option = Integer.parseInt(System.in.read());

            if(option == 1){ // Add pizza
                cart.addProduct( createPizza() );
            }
            else if(option == 2){ // Add burguer
                cart.addProduct( createBurguer() );
            } 
            else if(option == 3){ // Add hotdog
            
                cart.addProduct( createHotdog() );
            }
            else if(option == 4){ // Show cart
                cart.showProducts();
            }
            else if(option == 5){ // Empty Cart
                cart.emptyCart();
            }
            else if(option == 6){
                System.out.println("Exiting the store. Thank you!");
                break;
            }
        }
        while(true);
    }
}
