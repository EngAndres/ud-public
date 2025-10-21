/*
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

public class App {
    public static void main(String[] args)  {
        Vehicle v1 = new Vehicle("Ferrari", 350);
        v1.turnOff();
        v1.turnOn();
        v1.turnOff();

        System.out.println("==============");
        Car mcqueen = new Car(2008, "Cobra", "Shelby", 300);
        mcqueen.turnOn();
        mcqueen.gas();
        mcqueen.break_();
        mcqueen.turnOff();
        
        System.out.println("==============");
        Bike kawasaki = new Bike("blue", 600, "kawasaki", 50);
        kawasaki.turnOn();
        kawasaki.gas();
        kawasaki.break_();
        kawasaki.turnOff();
    }
}
