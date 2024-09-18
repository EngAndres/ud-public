/**
 * This file has class definition of a class for a simple calculator.
 * 
 * Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
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

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * This class represents the behavior of a simple concrete calculator
 * where methods from the abstract class are inherited, some improvements
 * and new functionalities are added.
 */
public class SimpleCalculatorSM extends AbstractCalculatorSM {

    private float memory;
    
    public SimpleCalculatorSM() {
        this.memory = 0;
    }

    /**
     * This method calculates the division between two numbers.
     *
     * This method takes two numbers, and calculates division using
     * native arithmetic operation, including validation of
     * zero-division.
     *
     * @param a Numerator of the division.
     * @param b Divisor of the division.
     * @return A float with the result of the division.
     */
    @Override
    public Float division(float a, float b) {
        float result;
        try {
            result = a / b;
        } catch (ArithmeticException e) {
            System.out.println("ERROR: " + e.getMessage());
            saveLog("ERROR: " + e.getMessage());
            result = Float.NaN; // Not a Number
        }
        return result;
    }

    /**
     * This is a method for power calculation.
     *
     * In this method the power is calculated using a loop
     * to apply multiplication in an iterative way.
     *
     * @param base Base of the power.
     * @param exponent Exponent of the power.
     * @return An integer with the result of the power.
     */
    @Override
    public int power(int base, int exponent) {
        int result;
        if (exponent == 0) {
            result = 1;
        } else {
            int temp = 1;
            for (int i = 0; i < exponent; i++) {
                temp *= base;
            }
            result = temp;
        }
        return result;
    }

    private void saveLog(String message) {
        try {
            String projectRoot = System.getProperty("user.dir");
            Path logFilePath = Paths.get(projectRoot, "log.txt");
            BufferedWriter writer = Files.newBufferedWriter(logFilePath, java.nio.file.StandardOpenOption.CREATE, java.nio.file.StandardOpenOption.APPEND);
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            String formattedDateTime = now.format(formatter);
            writer.write(formattedDateTime + " --- " + message);
            writer.newLine();
            writer.close();
        } catch (IOException e) {
            System.out.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}