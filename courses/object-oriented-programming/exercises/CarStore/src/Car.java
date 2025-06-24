/** This file has a class called Car, used as an
 * abstract class.
 * 
 * Author: Carlos Andrés Sierra <cavirguezs@udistrital.edu.co>
 */


public class Car {
    
    private Engine engine;
    private Chassis chassis;
    private Integer price;
    private String color;

    public Car(Integer cc, String chassisType, String color){
        this.color = color;
        this.engine = new Engine(cc);
        this.chassis = new Chassis(chassisType);
        this.calculatePrice();
    }

    private void calculatePrice(){
        int basePrice = 20;
        this.price = basePrice + this.engine.getPrice() + this.chassis.getPrice();
    }

    public String toString(){
        return "Car of " + this.engine.cc + " engine and " + this.color + " color";
    }

    public Boolean isSame(Integer cc, String chassis_type, String color){
        return this.engine.cc.equals(cc) && this.chassis.type.equals(chassis_type) && this.color.equals(color);
    }

    public Integer getPrice() {
        return this.price;
    }
}
