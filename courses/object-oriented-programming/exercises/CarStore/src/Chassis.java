

/**
 * This file has a class called Chassis, used as a
 * component of the car.
 * 
 * Author: Carlos Andrés Sierra <cavirguesz@udistrital.edu.co>
 */

public class Chassis {
    
    public String type;
    private Integer price;
    
    public Chassis(String type){
        this.type = type;
        this.calculatePrice();
    }

    /**
     * 
     */
    private void calculatePrice(){
        if(this.type.equals("Classical")){
            this.price = 40;
        }
        else if(this.type.equals("Sport")){
            this.price = 60;
        }   
    }

    /**
     * This method returns the price of the chassis.
     * 
     * @return chassis price
     */
    public Integer getPrice(){
        return this.price;
    }
}
