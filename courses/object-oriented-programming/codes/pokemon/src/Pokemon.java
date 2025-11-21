/*
 * This fila has an abstract class to represent a pokemon in the game.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

 /**
  * This class is an abstract class with some behaviors concretes and another
  * abstract to generalize a typical pokemon.
  */
public abstract class Pokemon {

    protected int attackDamage;
    protected int baseDefense;
    protected int health;
    
    protected Pokemon(int attackDamage, int baseDefense){
        this.attackDamage = attackDamage;
        this.baseDefense = baseDefense;
        this.health = 100;
    }

    /**
     * 
     * @return
     */
    public boolean isDefeated(){
        int minimumLevel = 5;
        return this.health < minimumLevel;
    }
    
    /**
     *  
     * @return
     */
    public Pokemon evolute(){
        return null;
    }

    public abstract int attack();

    public abstract void defense(String typeAdversary, int attackValue);

    public abstract void healthRecovery();
}