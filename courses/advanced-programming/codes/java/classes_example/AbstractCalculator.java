/**
 * This module is an example of an abstract class to define a calculator operations.
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

 /**
  * This class represents the behavior of an abstract calculator.
  */
public abstract class AbstractCalculator{
    public int sum(int a, int b){
        return a + b;
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
    public abstract float sum(float a, float b);

    public abstract Float division(float a, float b);
}