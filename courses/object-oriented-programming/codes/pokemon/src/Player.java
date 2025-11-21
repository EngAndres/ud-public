/*
 * 
 */

import java.util.ArrayList;

/**
 * 
 */
public class Player extends Character {
    
    protected ArrayList<Badge> badges;
        
    public Player(String name, Pokedex newPokedex){
        super(name, newPokedex);
        this.badges = new ArrayList<>();
    }

    public void catchPokemon(Pokemon newPokemon){
        if(this.pokedex.addPokemon(newPokemon)){
            System.out.println("Pokemon capturado.");
        } else {
            System.out.println("Pokemon fallido.");
        }
    }

    private boolean isBadgeRepeated(Badge newBagde){
        boolean response = false;

        for(Badge b: this.badges)
            if(newBagde.equals(b)){
                response = true;
                break;
            }
        
        return response;
    }

    public void winBadge(Badge newBadge){
        boolean result = this.isBadgeRepeated(newBadge);
        if(result){
            System.out.println("La insignia ya ha sido ganada por el jugador.");
        } else {
            this.badges.add(newBadge);
            System.out.println("La insignia ha sido agregada al jugador.");
        }
    }

    private boolean validateBagdeLevel(String type, int minLevel){
        boolean response = false;

        for(Badge b: this.badges)
            if(b.isValid(type, minLevel)){
                response = true;
                break;
            }

        return response;
    }

    public boolean isMaster(){
        boolean response = false;

        // badge Fire min Level 3
        response = this.validateBagdeLevel("fire",3);

        // badge Electric min Level 4
        if(response)
            response = this.validateBagdeLevel("electric", 4);

        // badge Rock min Level 2
        if(response)
            response = this.validateBagdeLevel("rock", 2);
        
        // badge Water min Level 3
        if(response)
            response = this.validateBagdeLevel("water", 3);
        
        return response;
    }
}
