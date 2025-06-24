import Product;
import java.util.ArrayList;
import java.util.List;
public class ShoopingCart {
    
    private List<Product> products = null;

    public ShoopingCart(){
        this.products = new ArrayList<>();
    }

    public boolean addProduct(Product product){
        try{
            this.products.add(product);
            return true;
        } catch (Exception e) {
            System.out.println("Error adding product: " + e.getMessage());  
            return false;
        }
    }

    public void showProducts(){
        if(this.products.isEmpty()){
            System.out.println("No products in the cart.");
            return;
        }
        
        for(Product product : this.products){
            System.out.println(product.toString());
        }
    }

    public Integer getCurrentPrice(){
        Integer acum = 0;

        for(Product product: this.products)
            acum += product.getPrice();

        return acum;
    }

    public void emptyCart(){
        this.products.clear();
    }
}
