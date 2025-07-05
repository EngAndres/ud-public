/**
 * This file has a mother class of the ArtWorks with the best reuse we
 * can design for this problem.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co> 
 */

public class ArtWork {

    private String title;
    private String artist;
    private Integer year;
    private String description;
    private String imagePath;

    public ArtWork(String title, String artist, Integer year, String description, String imagePath){
        this.title = title;
        this.artist = artist;
        this.year = year;
        this.description = description;
        this.imagePath = imagePath;
    }

    /**
     * This method returns the title of the artwork.
     * @return title of the artwork
     */
    public String getTitle(){
        return this.title;
    }

    /**
     * This method returns the artist of the artwork.
     * @return artist of the artwork
     */
    public String getArtist(){
        return this.artist;
    }

    /**
     * This method returns the year of the artwork.
     * @return year of the artwork
     */
    public Integer getYear(){
        return this.year;
    }

    /**
     * This method returns the description of the artwork.
     * @return description of the artwork
     */
    public String getDescription(){
        return this.description;
    }
    
    /**
     * This method returns the image path of the artwork.
     * @return image path of the artwork
     */
    public String getImagePath(){
        return this.imagePath;
    }
}
