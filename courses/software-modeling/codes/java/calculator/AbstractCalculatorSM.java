/**
 * This file has class definition of an abstract class for calculators.
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



/*
 * This class represents the behavior of an abstract calculator.
 */
public abstract class AbstractCalculatorSM {

    
    /**
     * This method sums two numerical values.
     *
     * This method takes two arguments, expected as numbers,
     * and calculates and returns the sum of those ones.
     *
     * @param a First number of the sum.
     * @param b Second number of the sum.
     * @return A float value with the result of the sum.
     */
    public float sum(float a, float b) {
        return a + b;
    }

    /**
     * This method applies subtraction between two numbers.
     *
     * This method takes two numbers received as arguments
     * and calculates the subtraction in the given order.
     *
     * @param a First number of the subtraction.
     * @param b Second number of the subtraction.
     * @return A float with the result of the subtraction.
     */
    public float rest(float a, float b) {
        return a - b;
    }

    /**
     * This method multiplies two numbers.
     *
     * This method takes two numbers provided as arguments
     * and calculates multiplication using native arithmetic operation.
     *
     * @param a First number of the multiplication.
     * @param b Second number of the multiplication.
     * @return A float with the result of the multiplication.
     */
    public float multiplication(float a, float b) {
        return a * b;
    }

    /**
     * This method calculates the division between two numbers.
     *
     * This method takes two numbers, and calculates division using
     * native arithmetic operation, but without validation of
     * zero-division.
     *
     * @param a Numerator of the division.
     * @param b Divisor of the division.
     * @return A float with the result of the division.
     */
    public Float division(float a, float b) {
        return a / b;
    }

    /**
     * This is an abstract method for power calculation.
     *
     * @param base Base of the power.
     * @param exponent Exponent of the power.
     * @return An integer with the result of the power.
     */
    public abstract int power(int base, int exponent);
}