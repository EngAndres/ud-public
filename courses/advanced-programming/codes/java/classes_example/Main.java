public class Main {
    private final String MENU = "\n\n1. Sum\n2. Division\n3. Exit\n";
    
    public static void main(String[] args) {
        Main main = new Main();
        
        Calculator calculator = new Calculator();
        int option;
        
        do{ 
            System.out.println(main.MENU);
            option = Integer.parseInt(System.console().readLine());
            
            switch(option){
                case 1 -> {
                    System.out.println("Enter the first number: ");
                    float a = Float.parseFloat(System.console().readLine());
                    System.out.println("Enter the second number: ");
                    float b = Float.parseFloat(System.console().readLine());
                    System.out.println("The result of the sum is: " + calculator.sum(a, b));
                }
                case 2 -> {
                    System.out.println("Enter the first number: ");
                    float a = Float.parseFloat(System.console().readLine());
                    System.out.println("Enter the second number: ");
                    float b = Float.parseFloat(System.console().readLine());
                    System.out.println("The result of the division is: " + calculator.division(a, b));
                }
                case 3 -> System.out.println("Bye!");
                default -> System.out.println("Invalid option.");
            }

        }
        while(option != 3);
    }
}
