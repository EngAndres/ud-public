/**
 * Photography class that extends the ArtWork class.
 * It represents a specific type of artwork that is a photograph.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

public class Photography extends ArtWork {

    private String style;

    public Photography(String title, String artist, Integer year, String description, String imagePath, String style){
        super(title, artist, year, description, imagePath);
        this.style = style;
    }

    /**
     * This method returns the style of the photograph.
     * @return style of the photograph
     */
    public String getStyle(){
        return this.style;
    }
}
