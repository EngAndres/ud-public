import Product;

class Chair implements Product {

    public String showDescription(){
        return "This is an example of a traditional chair";
    }

    public int calculateDeliveryDays(){
        return 2
    }
}