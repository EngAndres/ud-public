import java.util.List;
import java.util.ArrayList;

public class Catalog {

    public List<Car> cars;

    public Catalog(){
        this.cars = new ArrayList<>();
    }

    public void addCar(Integer cc, String chassis_type, String color){
        this.validateCar(cc, chassis_type, color);
        this.cars.add(new Car(cc, chassis_type, color));
    }

    public Boolean validateCar(Integer cc, String chassis_type, String color){
        for(Car car: this.cars){
            if(car.isSame(cc, chassis_type, color)) {
                return false;
            }
        }

        return true;
    }
}
