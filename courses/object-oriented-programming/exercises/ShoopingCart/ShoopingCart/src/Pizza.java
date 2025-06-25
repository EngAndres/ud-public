/*
 * This file contains the implementation of a Pizza product.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */



/**
 * This class represents a Pizza product in the store.
 * It implements the Product interface and provides
 * methods to calculate the price, check if it is
 * caduced, and to return a string representation of the pizza.
 */
public class Pizza implements Product {
    
    private Integer size = 0;
    private String flavor = "";
    private Integer price = 0;
    private Integer days = 0; 

    public Pizza(String flavor, Integer size, Integer days){
        this.size = size;
        this.flavor = flavor;
        this.days = days;
        this.calculatePrice();
    }

    private void calculatePrice(){
        int costPerUnit = 0;

        if(this.flavor.equals("Hawain"))
            costPerUnit = 40;
        else if(this.flavor.equals("Pepperoni"))
            costPerUnit = 50;
        else
            costPerUnit = 35;

        this.price = costPerUnit * this.size;
    }

    /**
     * This method checks if the pizza is caduced.
     * A pizza is considered caduced if it has been
     * more than 2 days since it was made.
     * 
     * @return true if the pizza is caduced, false otherwise.
     */
    public Boolean isCaduced(){
        return this.days > 2? true : false;
    }

    /**
     * This method returns the price of the pizza.
     * 
     * @return the price of the pizza.
     */
    public Integer getPrice(){
        return this.price;
    }

    /**
     * This method returns a string representation of the pizza.
     * 
     * @return a string describing the pizza.
     */
    public String toString(){
        return "This pizza is " + this.flavor + 
               " with size " + this.size + 
               " and costs " + this.price + ".";
    }
}
