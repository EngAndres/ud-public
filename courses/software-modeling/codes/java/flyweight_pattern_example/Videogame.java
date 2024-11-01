import TreeImage;
import java.util.HashMap;
import java.util.ArrayList;

public class VideoGame{

    private HashMap<String, TreeImage> images = new HashMap<String, Image>();
    private ArrayList<Tree> trees = new ArrayList<Tree>();

    public void addTrees(int x, int y, String typeTree){
        if(!images.containsKey(typeTree)){
            this.images.put(typeTree, new TreeImage(typeTree, "path_to_tree_"+typeTree+".png"));
        
        this.trees.add(new Tree(x, y, this.images.get(typeTree)));
    }

    public void drawTrees(){
        for(Tree tree : this.trees){
            tree.draw();
        }
    }
}