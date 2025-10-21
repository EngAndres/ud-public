/*
 * This file has an interface to generalize the actions
 * all the characters of the video game should have.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */
public interface MortalKombatCharacter {
    
    public abstract int launchPunch();

    public abstract int launchKick();

    public abstract boolean launchPower();
}
