/*
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

 /**
  * This class represents the behavior of a bike in the application.
  */
public class Bike extends Vehicle {

    public String color;
    public int cc = 0;

    public Bike(String color, int cc, String brand, double maxSpeed){
        super(brand, maxSpeed);
        this.color = color;
        this.setCC(cc);
    }

    /**
     * This method sets the cc of a car, just letting to setup
     * once, and validating cc is a positive number.
     * @param cc
     */
    public void setCC(int cc){
        if(this.cc == 0){ 
            if(cc > 0){
                this.cc = cc;
            }    
            else{
                System.out.println("CC cannot    be negative.");
            }
        }
        else{
            System.out.println("Motor bike has already the setup for the cc.");
        }
    }
    
    /**
     * This method presses the gas pedal of the bike.
     */
    public void gas(){
        System.out.println("Rnnnnnn bike!");
    }
    
    /**
     * This method presses the brake pedal of the bike.
     */
    public void break_(){
        System.out.println("Shshshsh bike!");
    }
}
