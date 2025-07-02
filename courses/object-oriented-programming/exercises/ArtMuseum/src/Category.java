

/**
 * This file has a class called Cateogry as a domain information
 * part of the application.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

 public class Category {

    private String name;
    private String description;

    public Category(String name, String description) {
        this.name = name;
        this.description = description;
    }  

    /**
     * This method returns the name of the category.
     * 
     * @return category's name
     */
    public String getName(){
        return this.name;
    }

    /**
     * Data to print of the object.
     */
    public String toString(){
        return "Name: " + this.name + ". Description: " + this.description;
    }
 }