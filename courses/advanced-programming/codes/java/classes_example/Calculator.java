/**
 * This module is an example of a concrete class to define a calculator operations.
 * 
 * Copyright (C) 2024  Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;




public class Calculator extends AbstractCalculator{

    private int memory;

    public Calculator(){
        this.memory = 0;
    }

    /**
     * This method sums two integer numbers.
     *
     * In this method a couple of integers are taken and sum had been calculated
     * independing of size and sign.
     *   
     * Args:
     *      a (int): Fisrt number to be used in the addition.
     *      b (int): Second number to be used in the addition.
     *
     * Returns:
     *      An integer with the result of sum the arguments given.
     */
    @Override
    public float sum(float a, float b){
        return a + b;
    }

    /**
     * This method divides two decimal numbers.
     *
     * In this method a couple of decimals are taken and 
     * division had been calculated.
     *   
     * Args:
     *      a (float): Fisrt number to be used in the division.
     *      b (float): Second number to be used in the division.
     *
     * Returns:
     *      An float with the result of division the arguments given.
     */
    @Override
    public Float division(float a, float b){
        Float result = null;
        try {
            if (b == 0) {
                throw new ArithmeticException("Division by zero");
            }
            result = a / b;
        } catch (Exception e) {
            System.out.println("ERROR: " + e.getMessage());
            this.saveLog("ERROR: " + e.getMessage());
        }
        return result;
    }

    private void saveLog(String message){
        try {
            BufferedWriter writer = new BufferedWriter(new FileWriter("log.txt"));
            writer.write(message);
            writer.close(); 
        } catch (IOException e) {
            System.out.println("An error occurred while writing to the file: " + e.getMessage());
        }
    }
}