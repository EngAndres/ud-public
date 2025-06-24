import Product;

/**
 * This class represents a Hotdog product in the store.
 * It implements the Product interface and provides
 * methods to calculate the price, check if it is
 * caduced, and to return a string representation of the hotdog.
 */
public class Hotdog implements Product{

    private Integer price = 0;
    private String sausage = null;
    private Integer days = 0;

    public Hotdog(String sausage, Integer days) {
        this.days = days;
        this.sausage = sausage;

        if(this.sausage.equals("American")) 
            this.price = 400;
        else if(this.sausage.equals("Choriperro"))
            this.price = 500;
    }

    /**
     * This method checks if the hotdog is caduced.
     * A hotdog is considered caduced if it has been
     * more than 3 days since it was made.
     * 
     * @return true if the hotdog is caduced, false otherwise.
     */
    public  Boolean isCaduced() {
        if(this.days > 3) 
            return true;
        else 
            return false;
    }

    /**
     * This method returns the price of the hotdog.
     * 
     * @return the price of the hotdog.
     */
    public Integer getPrice() {
        return this.price;
    }

    /**
     * This method returns a string representation of the hotdog.
     * 
     * @return a string describing the hotdog.
     */
    public String toString() {
        return "This is a hotdog with " + this.sausage + 
               " sausage. Price: " + this.price + " dollars.";
    }
    
}
