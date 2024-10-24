import TV100SUD;
import TV120SUD; 
import UniversalControl;

public class Client{

    public static void main(String[] args){

        String model = "100US"; // TODO this should be choosen by the user

        if (model.equals("100US"))
            TVDevice tv = new TV100SUD(); // Liskov
        else if (model.equals("120US"))
            TVDevice tv = new TV120SUD(); // Liskov
        
        UniversalControl control = new UniversalControl(tv);
    }
}