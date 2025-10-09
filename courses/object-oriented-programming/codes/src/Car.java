import java.util.List;
import java.util.ArrayList;

public class Car {
    
    public List<Sticker> stickers = null;
    public Engine engine;

    public Car(Engine engine){
        this.stickers = new ArrayList<>();
        this.engine = engine;
    }

    public void addSticker(Sticker newStiker){
        newStiker.glue_to_car();
        this.stickers.add(newStiker);
    }

    /**
     * This method show all the stickers in the car.
     */
    public void showStickers(){
        if(this.stickers.isEmpty()){
            System.out.println("=== No stickers ===");
        }
        else{
            for(Sticker s: this.stickers){
                System.out.println(s.text);
            }
        }
    }
    public void paintCar(){
        this.stickers.clear();
    }

    public void turnOn(){
        System.out.println("Turning on the car");
        this.engine.start();
    }

    public void turnOff(){
        System.out.println("Turning off the car");
        this.engine.stop();
    }
}       
