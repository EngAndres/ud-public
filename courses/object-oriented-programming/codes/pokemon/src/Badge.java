public class Badge {
    
    private String element;
    private int level;

    public Badge(String element, int level){
        this.element = element;
        this.level = level;
    }

    public boolean isValid(String type, int level){
        return this.element.equals(type) && this.level >= level;
    }
}
