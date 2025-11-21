/*
 * 
 */

import java.util.ArrayList;

/**
 * 
 */
public class Pokedex {
    private ArrayList<Pokemon> pokemones;

    public Pokedex(){
        this.pokemones = new ArrayList<>();
    }

    public boolean addPokemon(Pokemon newPokemon){
        boolean isFound = false;
        for(Pokemon p: this.pokemones)
            if(p.equals(newPokemon)){
                isFound = true;
                break;
            }
        
        if(!isFound)
            this.pokemones.add(newPokemon);

        return isFound;
    }

    public Pokemon getPokemon(){
        return this.pokemones.get(0);
    }
}