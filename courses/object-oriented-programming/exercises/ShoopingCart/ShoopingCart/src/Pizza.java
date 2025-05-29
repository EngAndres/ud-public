import Product;

public class Pizza implements Product {
    
    private Integer size = 0;
    private String flavor = "";
    private Integer price = 0; 

    public Pizza(String flavor, Integer size){
        this.size = size;
        this.flavor = flavor;
        this.calculatePrice();
    }

    private void calculatePrice(){
        int costPerUnit = 0;

        if(this.flavor == "Hawain")
            costPerUnit = 2;
        else if(this.flavor == "Pepperoni")
            costPerUnit = 3;

        this.price = costPerUnit * this.size;
    }

    public Boolean isCaduced(){
        return false;
    }

    public Integer getPrice(){
        return this.price;
    }

    public String toString(){
        return "";
    }
}
