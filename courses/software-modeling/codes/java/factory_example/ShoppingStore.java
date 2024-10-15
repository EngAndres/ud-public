import FactoryProducts;
import Product;
import Shoes;
import Chair;

public class ShoppingStore implements FactoryProducts {

    public Product createProduct(String type){
        if(type == "chair")
            return new Chair();
        else if(type == "shoes")
            return new Shoes();
        else
            return null;
    }
}