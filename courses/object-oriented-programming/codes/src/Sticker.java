public class Sticker {

    public String text;
    public String color;

    public Sticker(String text, 
                    String color){
        this.text = text;
        this.color = color;
    }

    public void glue_to_car(){
        System.out.println("Me acabo de pegar al carro.");
    }
}
