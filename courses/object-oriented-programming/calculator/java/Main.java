import calculator.java.Calculator;

public class Main {
    
    public static void main(String[] args){
        // Object instance
        Calculator calculator = new Calculator();

        String MENU = "1.Sumar\n2.Restar\n3.Multiplicar\n4.Dividir\n5.Salir";
        int option = 0;

        do{
            System.out.println(MENU);
            System.out.print("Elige una opción: ");
            option = Integer.parseInt(System.console().readLine());

            switch(option){
                case 1:
                    System.out.print("Introduce el primer número: ");
                    Double num1 = Double.parseDouble(System.console().readLine());
                    System.out.print("Introduce el segundo número: ");
                    Double num2 = Double.parseDouble(System.console().readLine());
                    System.out.println("La suma es: " + calculator.sum(num1, num2));
                    break;
                case 2:
                    System.out.print("Introduce el primer número: ");
                    num1 = Double.parseDouble(System.console().readLine());
                    System.out.print("Introduce el segundo número: ");
                    num2 = Double.parseDouble(System.console().readLine());
                    System.out.println("La resta es: " + calculator.substract(num1, num2));
                    break;
                case 3:
                    System.out.print("Introduce el primer número: ");
                    num1 = Double.parseDouble(System.console().readLine());
                    System.out.print("Introduce el segundo número: ");
                    num2 = Double.parseDouble(System.console().readLine());
                    System.out.println("La multiplicación es: " + calculator.multiplication(num1, num2));
                    break;
                case 4:
                    System.out.print("Introduce el primer número: ");
                    num1 = Double.parseDouble(System.console().readLine());
                    System.out.print("Introduce el segundo número: ");
                    num2 = Double.parseDouble(System.console().readLine());
                    if(num2 != 0){
                        System.out.println("La división es: " + calculator.division(num1, num2));
                    }else{
                        System.out.println("No se puede dividir entre cero");
                    }
                    break;
                case 5:
                    System.out.println("Saliendo...");
                    break;
                default:
                    System.out.println("Opción no válida");
            }
        }
        while(option != 5)
    }
}
