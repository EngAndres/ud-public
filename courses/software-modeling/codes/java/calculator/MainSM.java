/**
 * This file has a simple CLI for calculator manipulation.
 *
 * This file is part of JCalculator-UD.
 *
 * JCalculator-UD is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * JCalculator-UD is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with JCalculator-UD. If not, see <https://www.gnu.org/licenses/>.
 */


import java.util.Scanner;

public class MainSM {

    private final String MENU = "1. Sumar\n2. Restar\n3. Multiplicar\n4. Dividir\n5. Potencia\n6. Salir\n\n";


    public static void main(String[] args) {
        MainSM main = new MainSM();

        Scanner scanner = new Scanner(System.in);
        SimpleCalculatorSM calculator = new SimpleCalculatorSM();

        
        int option;
        do {
            System.out.print(main.MENU);
            option = scanner.nextInt();

            switch (option) {
                case 1 -> {
                    System.out.print("Add first number of the sum: ");
                    float a1 = scanner.nextFloat();
                    System.out.print("Add second number of the sum: ");
                    float b1 = scanner.nextFloat();
                    System.out.println("Result: " + calculator.sum(a1, b1));
                }
                case 2 -> {
                    System.out.print("Add first number of the rest: ");
                    float a2 = scanner.nextFloat();
                    System.out.print("Add second number of the rest: ");
                    float b2 = scanner.nextFloat();
                    System.out.println("Result: " + calculator.rest(a2, b2));
                }
                case 3 -> {
                    System.out.print("Add first number of the multiplication: ");
                    float a3 = scanner.nextFloat();
                    System.out.print("Add second number of the multiplication: ");
                    float b3 = scanner.nextFloat();
                    System.out.println("Result: " + calculator.multiplication(a3, b3));
                }
                case 4 -> {
                    System.out.print("Add first number of the division: ");
                    float a4 = scanner.nextFloat();
                    System.out.print("Add second number of the division: ");
                    float b4 = scanner.nextFloat();
                    System.out.println("Result: " + calculator.division(a4, b4));
                }
                case 5 -> {
                    System.out.print("Add base of the power: ");
                    int base = scanner.nextInt();
                    System.out.print("Add exponent of the power: ");
                    int exponent = scanner.nextInt();
                    System.out.println("Result: " + calculator.power(base, exponent));
                }
                case 6 -> System.out.println("Exiting...");
                default -> System.out.println("Please, choose a valid option.");
            }
        } while (option != 6);

        scanner.close();
    }
}