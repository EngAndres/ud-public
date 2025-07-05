/**
 * This class represents an exhibition in an art museum.
 * It is a placeholder for future implementation and does not contain any properties or methods yet.
 * 
 * This method will be used to add artworks to the exhibition.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

import java.util.ArrayList;
import java.util.List;

public class Exhibition {
    
    private String name;
    private Category category;
    private List<ArtWork> artWorks;

    public Exhibition(String name, Category category){
        this.name = name;
        this.category = category;
        this.artWorks = new ArrayList<>();
    }

    /**
     * This method returns the name of the exhibition.
     * 
     * @return the name of the exhibition
     */
    public String getName(){
        return this.name;
    }

    /**
     * This method adds an art work to the exhibition.
     * 
     * @param the art work to be added
     */
    public void addArtWork(ArtWork artWork) {
        this.artWorks.add(artWork);
    }

    /**
     * This method returns the list of art works reported for the exhibition.
     * 
     * @return list of art works in the exhibition
     */
    public List<ArtWork> getArtWorks(){
        return this.artWorks;
    }


    public String toString(){
        StringBuilder sb = new StringBuilder();
        sb.append("Exhibition Name: ").append(this.name).append("\n");
        sb.append("Category: ").append(this.category.getName()).append("\n");
        sb.append("Art Works:\n");
        for (ArtWork artWork : artWorks) {
            sb.append(artWork.toString()).append("\n");
        }
        return sb.toString();
    }
}
