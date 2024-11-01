import TreeImage;

public class Tree{
    private int x;
    private int y;
    private TreeImage image;

    public Tree(int x, int y, TreeImage image){
        this.x = x;
        this.y = y;
        this.image = image;
    }

    public void draw(){
        this.image.draw(this.x, this.y);
    }
}