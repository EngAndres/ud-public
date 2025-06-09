import Product;

/**
 * This class represents a Burguer product in the store.
 * It implements the Product interface and provides
 * methods to calculate the price, check if it is
 * caduced, and to return a string representation of the burger.
 */
public class Burguer implements Product {
    
    private Integer price = 0;
    private Integer weight = 0;

    public Burguer(Integer weight) {
        this.weight = weight;
        this.calculatePrice(5); 
    }

    private void calculatePrice(int perGramPrice) {
        this.price = this.weight * perGramPrice; 
    }

    /**
     * This method checks if the burger is caduced.
     * 
     * @return false, as burgers are not considered caduced.
     */
    public Boolean isCaduced() {
        return false;
    }

    /**
     * This method returns the price of the burger.
     * 
     * @return the price of the burger.
     */
    public Integer getPrice() {
        return this.price;
    }

    /**
     * This method returns a string representation of the burger.
     * 
     * @return a string describing the burger.
     */
    public String toString() {
        return "This is a burger weighing " + this.weight + 
                " grams. Price: " + this.price + " dollars.";
    }
}
