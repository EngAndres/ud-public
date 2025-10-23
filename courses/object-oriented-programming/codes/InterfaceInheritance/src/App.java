import java.util.Scanner;

public class App {

    public static int chooseAction(String characterName){      
        int action = -1;
        Scanner sc = new Scanner(System.in);
        do{
            System.out.println("Choose action for " + characterName 
                    + ":\n1. Punch\n2: Kick\n");
            action = Integer.parseInt(sc.next());
        }while(action < 1 && action > 2);
        return action;
    }

    public static void main(String[] args) throws Exception {
        Kitana kitana = new Kitana();
        LiuKahn liuKahn = new LiuKahn(18, 10);

        boolean gameOver = false;

        while(!gameOver){
            if(chooseAction("Kitana") == 1){
                liuKahn.sufferDamage(kitana.launchPunch());
            } else {
                liuKahn.sufferDamage(kitana.launchKick());
            }
            kitana.sufferDamage(liuKahn.launchKick());
            
            gameOver = kitana.isDead();

            System.out.println("Both characters are alive. " + gameOver);

            kitana.sufferDamage(liuKahn.launchKick());
            kitana.sufferDamage(liuKahn.launchKick());
            kitana.sufferDamage(liuKahn.launchKick());
            kitana.sufferDamage(liuKahn.launchKick());
         
            gameOver = kitana.isDead();
            System.out.println("Massive attack over kitana. " + gameOver);
        }
    }
}
