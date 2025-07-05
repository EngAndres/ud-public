/**
 * This file has a class called Sculpture as a domain information
 * part of the application.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

public class Sculpture extends ArtWork {

    private String material;

    public Sculpture(String title, String artist, Integer year, String description, String imagePath, String material){
        super(title, artist, year, description, imagePath);
        this.material = material;
    }

    /**
     * This method returns the material used in the sculpture.
     * @return material of the sculpture
     */
    public String getMaterial(){
        return this.material;
    }
}
