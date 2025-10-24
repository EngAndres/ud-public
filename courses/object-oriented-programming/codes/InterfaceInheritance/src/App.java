import java.util.Scanner;
import java.util.ArrayList;
public class App {

    public static Character getCharacter(int option){
        Character c = null;
        switch(option){
            case 1:
                c = new Kitana("Kitana");
                break;
            case 2:
                c = new LiuKahn("Liu Kahn", 20, 12);
                break;
            case 3:
                c = new Sonia("Sonia", 15, 15); 
                break; 
        }
        return c;
    }

    public static ArrayList<Character> chooseCharacters(){
        int action = -1;
        String options = "1. Kitana\t2. Liu Kahn\t3.Sonia";
        
        ArrayList<Character> characters = new ArrayList<Character>();
        Scanner sc = new Scanner(System.in);

        // Choose Player 1
        do{
            System.out.println("Choose Player 1:\n" + options);
            action = sc.nextInt();
        }while(action < 1 || action > 3);
        characters.add( getCharacter(action) );

        // Choose Player 2
        do{
            System.out.println("Choose Player 2:\n" + options);
            action = sc.nextInt();
        }while(action < 1 && action > 3);
        characters.add( getCharacter(action) );

        return characters;
    }

    public static int chooseAction(String characterName){      
        int action = -1;
        Scanner sc = new Scanner(System.in);
        do{
            System.out.println("\nChoose action for " + characterName 
                    + ":\n1. Punch\n2: Kick");
            action = Integer.parseInt(sc.next());
        }while(action < 1 || action > 2);
        return action;
    }

    public static void main(String[] args) {
        boolean gameOver = false;
        int turn = 0; 
        int nextTurn = 1;

        ArrayList<Character> characters = chooseCharacters();

        while(!gameOver){
            if(chooseAction(characters.get(turn).name) == 1){
                characters.get(nextTurn).sufferDamage( characters.get(turn).launchPunch());
            } else {
                characters.get(nextTurn).sufferDamage( characters.get(turn).launchKick());
            }
            gameOver = characters.get(nextTurn).isDead();

            if(gameOver){
                System.out.println(characters.get(nextTurn).name + 
                    " is dead. " + characters.get(turn).name + 
                    " wins.");
            } else {
                if(turn == 1){
                    turn = 0;
                    nextTurn = 1;
                } else {
                    turn = 1;
                    nextTurn = 0;
                }
            }
        }
    }
}