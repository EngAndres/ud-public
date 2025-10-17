/*
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

/**
 * This class represents the behavior of a vehicle in the app.
 * This one generalize any vehicle as car, bike, or airplane.
 */
public class Vehicle{

    public String brand;
    public double maxSpeed;
    public boolean on;

    /**
     * This is the constructor of a vehicle.
     * @param brand
     * @param maxSpeed
     */
    public Vehicle(String brand, double maxSpeed){
        this.brand = brand;
        this.setMaxSpeed(maxSpeed);
        this.on = false; // default value
    }

    /**
     * This method sets the value of the maximum speed of the
     * vehicle, valifating than there is no negative speeds.
     * @param maxSpeed
     */
    public void setMaxSpeed(double maxSpeed){
        if(maxSpeed < 0){
            System.out.println("Error. Speed cannot be negative.");
        }
        else{
            this.maxSpeed = maxSpeed;
        }
    }

    /**
     * This method turns on the vehicle if it is off.
     */
    public void turnOn(){
        if(this.on){
            System.out.println("Vehicle is already on.");
        }
        else {
            System.out.println("Vehicle is turning on!");
            this.on = true;
        }
        
    }

    /**
     * This method turns off the vehicle if it is on.
     */
    public void turnOff(){
        if(!this.on){
            System.out.println("Vehicle is already off");    
        }
        else {
            this.on = false;
            System.out.println("Vehicle is turning off!");
        }
    }
}
