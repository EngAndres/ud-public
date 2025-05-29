/**
 * This file contains an interface to define the structure
 * of all the products in the store.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

/*
 * This is an interface for Products in the store.
 */
public interface Product  {

    public abstract Boolean isCaduced();

    public abstract String toString();

    public abstract Integer getPrice();
}
