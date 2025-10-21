/*
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

/**
 * This class represents the behavior of a car in the application.
 */
public class Car extends Vehicle {

    public int year;
    public String model;

    public Car(int year, String model, String brand, double maxSpeed){
        super(brand, maxSpeed);
        this.model = model;
        this.setYear(year);
    }
    
    /**
     * This method sets the year of the car validating than
     * the year should be greater or equal than 1900.
     * @param newYear
     */
    public void setYear(int newYear){
        if(newYear >= 1900){
            this.year = newYear;
        }
        else{
            System.out.println("Error. The value of the year is wrong.");
        }
    }

    /**
     * This method presses the gas pedal of the car.
     */
    public void gas(){
        System.out.println("Rnnnnnn car!");
    }
    
    /**
     * This method presses the brake pedal of the car.
     */
    public void break_(){
        System.out.println("Shshshsh car!");
    }
}
