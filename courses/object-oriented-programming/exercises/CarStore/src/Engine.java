/**
 * This file has a class called Engine who represents the
 * behavior of an engine component of a car.
 * 
 * Author: Carlos Andrés Sierra <cavirguesz@udistrital.edu.co>
 */

public class Engine {
    
    private Integer price;
    private Integer weight;
    public Integer cc;

    public Engine(Integer cc){
        this.cc = cc;
        this.calculatePrice();
        this.calculateWeight();
    }

    /**
     * This method calculates the price of the engine based on its cc.
     * The price is calculated as 5 times the cc.
     */
    private void calculatePrice(){
        int costPerCc = 5;
        this.price = costPerCc * this.cc;
    }

    /**
     * This method calculates the weight of the engine based on its cc.
     * The weight is calculated as 2 times the cc.
     */
    private void calculateWeight(){
        int weightPerCc = 2;
        this.weight = weightPerCc * this.cc;
    }

    /**
     * This method returns the price of the engine.
     * 
     * @return engine price
     */
    public Integer getPrice(){
        return this.price;
    }

    /**
     * This method returns the weight of the engine.
     * 
     * @return engine weight
     */
    public Integer getWeight(){
        return this.weight;
    }
}
