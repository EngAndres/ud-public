package association;
public class Engine {
    
    public int cc;
    public int potency;
    public String brand;
    public int consume;

    public Engine(String brand, int cc, int potency){
        this.brand = brand;
        this.cc = cc;
        this.potency = potency;
        this.calculateConsume();
    }

    private void calculateConsume(){
        this.consume = 1000 * this.cc;
    }  
    
    public void start(){
        System.out.println("ruuuuuuuuun!");
    }

    public void stop(){
        System.out.println("chchchch!");
    }

    public void info(){
        System.out.println("Brand: " + this.brand + "\tCC: " + this.cc +
                            "\tPotency: " + this.potency + "\tConsume: " + this.consume);
    }
}
