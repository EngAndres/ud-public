import Product;

class Shoes implements Product {

    public String showDescription(){
        return "These shoes are made for walking";
    }

    public int calculateDeliveryDays(){
        return 3;
    }
}