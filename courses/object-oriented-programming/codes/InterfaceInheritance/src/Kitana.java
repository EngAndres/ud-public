/*
 * This a class of an character called Kitana.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

/**
 * This class represent the character Kitana in the video game.
 * This one inheriths from CharacterLife to handle life properties, 
 * and from MortalKombatCharacter to implements some attacks.
 */
public class Kitana extends Character implements MortalKombatCharacter{

    /**
     * Zero-parameters constructor.
     */
    public Kitana(String name){
        super(name);
    }

    /**
     * This method means a kick attack from Kitana.
     */
    public int launchKick(){
        System.out.println("Kitana has launched a kick.");
        return 15;
    }

    /**
     * This method means a punch attack from Kitana.
     */
    public int launchPunch(){
        System.out.println("Kitana has launched a punch");
        return 5;
    }

    /**
     * Kitana has not power.
     */
    public boolean launchPower(){
        return false;
    }
}