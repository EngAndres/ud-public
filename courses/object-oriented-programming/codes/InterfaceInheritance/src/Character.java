/*
 * This file has a mother class with some common behaviors for all
 * the characters related with the life level.
 */

/**
 * This class represents the commom behavior related to life of
 * a videogame character.
 */
public class Character implements MortalKombatCharacter {
    private int life;
    public String name;

    public Character(String name){
        this.name = name;
        this.life = 100;
    }

    /**
     * This method reduces the life of a character based
     * on the damage level.
     * @param damage
     */
    public void sufferDamage(int damage){
        this.life -= damage;
    }

    /**
     * This method checks if a character is still with some life.
     * @return true if character is dead
     */
    public boolean isDead(){
        return this.life < 0 ? true : false;
    }

    public int launchPunch() {
        return -1;
    }

    public int launchKick() {
        return -1;
    }

    public boolean launchPower() {
        return false;
    }
}