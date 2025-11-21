import java.util.Scanner;
import java.util.ArrayList;
import java.util.Random;
public class App {

    static ArrayList<Gym> gyms = new ArrayList<>();
    static ArrayList<Pokemon> wildPokemons = new ArrayList<>();
    static ArrayList<IClinic> clinics = new ArrayList<>();
    
    public static Gym addGym(){
        System.out.println("\n\n== AGREGAR GIMNASIO");
        Scanner sc = new Scanner(System.in);
        
        System.out.print("Escriba el nombre del gimnasio:");
        String name = sc.next();
        
        System.out.print("\nEscriba el tipo del gimnasio (agua, electrico, roca, fuego):");
        String type = sc.next();
        
        System.out.print("\nEscriba el nombre del lider:");
        String leaderName = sc.next();

        Character leader = new Character(leaderName, new Pokedex());
        
        return new Gym(name, type, leader);
    }

    public static Pokemon addWildPokemon(){
        String[] types = {"fire", "water", "electric", "rock"};
        Random r = new Random();
        String type = types[ r.nextInt(types.length) ];
        int baseDefense = r.nextInt(5, 10);
        int attackDamage = r.nextInt(8, 15);

        if(type.equals("fire"))
            return new FirePokemon(attackDamage, baseDefense);
        else if(type.equals("water"))
            return new WaterPokemon(attackDamage, baseDefense);
        else if(type.equals("electric"))
            return new ElectricPokemon(attackDamage, baseDefense);
        else if(type.equals("rock"))
            return new RockPokemon(attackDamage, baseDefense);
        return null;
    }

    public static IClinic addClinic(){
        Scanner sc = new Scanner(System.in);
        System.out.println("Seleccione el tipo de clinica:\n1. Pequenia\n2. Grande");
        int type = sc.nextInt();
        if(type == 1){
            System.out.println("Ingrese nombre de enfermera: ");
            String nurse = sc.nextLine();
            return new SmallClinic(nurse);
        } else if(type == 2) {
            System.out.println("Ingrese nombre de medico: ");
            String medicalDoctor = sc.nextLine();
            return new BigClinic(medicalDoctor);
        } else {
            System.out.println("Valor erroneo para el tipo de clinica.");
            return null;
        }
    }

    public static void init(){
        //default gym
        Character leader = new Character("Bruce", new Pokedex());
        Gym gym = new Gym("Pueblo Paleta", "roca", leader);
        gyms.add( gym );

        // first 5 gyms by user
        int initGyms = 5;
        for(int i = 0; i < initGyms; i++)
            gyms.add( addGym() );
        
        // add 10 pokemons
        int initPokemons = 10;
        for(int i = 0; i < initPokemons; i++)
            wildPokemons.add( addWildPokemon() );

        // add 3 clinics
        int initClinics = 3;
        for(int i = 0; i < initClinics; i++)
            clinics.add( addClinic() );
    }

    public static void main(String[] args) throws Exception {
        init();

        Scanner sc = new Scanner(System.in);
        System.out.println("BIENVENIDO AL POKEMON UD.\nIngrese nombre del jugador:");
        String name = sc.nextLine();
        Player player = new Player(name, new Pokedex());
        
    }
}
