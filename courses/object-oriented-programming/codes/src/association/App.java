import association.Car;
import association.Engine;
import association.Sticker;

public class App {
    public static void main(String[] args)  {
        
        Engine sport = new Engine("Masserati", 5000, 600);

        Car myCacharrito = new Car(sport);
        System.out.println("Moment 0");
        myCacharrito.showStickers();

        Sticker st1 = new Sticker("I <3 UD", "yellow");
        Sticker st2 = new Sticker("Hello UD.", "red");

        System.out.println("\nMoment 1:");
        myCacharrito.addSticker(st2);
        myCacharrito.addSticker(st1);
        myCacharrito.showStickers();

        System.out.println("\nMoment 2:");
        myCacharrito.engine.info();

        System.out.println("\nMoment 3:");
        myCacharrito.turnOn();

        System.out.println("\nMoment 4:");
        myCacharrito.turnOff();
    }
}
