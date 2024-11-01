public class TreeImage{

    private String image_path;
    private String name;

    public TreeImage(String name, String image_path){
        this.image_path = image_path;
        this.name = name;
    }

    public void draw(int x, int y){
        System.out.println("Drawing a tree if name " 
        + this.name + " at position " + x + ", " + y)
    }
}