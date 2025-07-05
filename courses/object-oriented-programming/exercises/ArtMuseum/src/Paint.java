/**
 * This class represents a Paint object in an art museum.
 * It extends the ArtWork class and includes additional properties specific to paintings.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

public class Paint extends ArtWork{
    
    private String technique;

    public Paint(String title, String artist, Integer year, String description, String imagePath, String technique){
        super(title, artist, year, description, imagePath);
        this.technique = technique;
    }

    /**
     * This method returns the technique used in the painting.
     * @return technique of the painting
     */
    public String getTechnique(){
        return this.technique;
    }   
}
