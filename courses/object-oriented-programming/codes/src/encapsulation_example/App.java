package example_encapsulation;
public class App {
    public static void main(String[] args) {
        System.out.println("Students UD!");
        
        Student pepita = new Student("Pepita", 7.1, 20); 
        Student pepito = new Student("Pepito", 2.3, -19);

        System.out.println("Pepita: " + pepita.comoVoy());
        System.out.println("Pepito: " + pepito.comoVoy());
    }
}
