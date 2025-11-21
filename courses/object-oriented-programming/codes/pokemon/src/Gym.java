/*
 * 
 */

 /**
  * 
  */
public class Gym {
    
    public String name;
    public String type;
    public Character leader;

    public Gym(String name, String type, Character leader){
        this.name = name;
        this.type = type;
        this.leader = leader;
    }

    public boolean fight(Pokemon playerPokemon){
        boolean playerWin = false;
        boolean game = true;
        Pokemon gymPokemon = leader.pokedex.getPokemon();

        int turn = 0; // 0 is player turn; 1 is game turn
        while(game){
            if(turn == 0) {
                gymPokemon.defense("", playerPokemon.attackDamage);
                if(gymPokemon.isDefeated()){
                    playerWin = true;
                    game = false;
                }
                turn = 1;     
            } else {
                playerPokemon.defense(this.type, gymPokemon.attackDamage);
                if(playerPokemon.isDefeated())
                    game = false;
                turn = 0;
            }
        }

        return playerWin;
    }
}
