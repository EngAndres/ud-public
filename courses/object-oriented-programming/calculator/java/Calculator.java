/**
 * This is a simple example of a calculador as an object 
 */
public class Calculator {

    private Double memory;

    public Calculator(){
        this.memory = 0.0;
    }

    /**
     * This method makes an addition to another number.
     * 
     * @param a1: First number in the addition
     * @param b2: Second number in the addition
     * 
     * @return The sum of the two numbers
     */
    public Double sum(Double a1, Double b2){
        return a1 + b2;
    }

    /**
     * This method makes a substraction of the second
     * number from the first number.
     * 
     * @param num1: First number of the substraction
     * @param num2: Second mumber of the substraction
     * 
     * @return The substracion of two numbers
     */
    public Double substract(Double num1, Double num2){
        return num1 - num2
    }

    /**
     * This method multiplies two numbers.
     * 
     * @param num1: First number of the multiplication
     * @param num2: Second number of the multiplication
     * 
     * @return A number with the result of the multiplication
     */
    public Double multiplication(Double num1, Double num2){
        return num1 * num2;
    }

    /**
     * This method makes the division of two numbers.
     * 
     * @param num1: enumerator of the division
     * @param num2: denominator of the division
     * 
     * @return The result of the division, if num2 is different to zero
     */
    public Double division(Double num1, Double num2){
        try{
            return num1 / num2;
        }
        catch(Exception e){
            System.out.println("Error in the division." + e);
        }
    }
}