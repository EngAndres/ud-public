/*
 * This a class of an character called Sonia.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

/**
 * This class represent the character Sonia in the video game.
 * This one inheriths from CharacterLife to handle life properties, 
 * and from MortalKombatCharacter to implements some attacks.
 */
public class Sonia extends Character implements MortalKombatCharacter{

    private int kickDamage;
    private int punchDamage;
    private int powerAcum;

    public Sonia(String name, int kickDamage, int punchDamage){
        super(name);
        this.kickDamage = kickDamage;
        this.punchDamage = punchDamage;
        this.powerAcum = 0;
    }

    /**
     * This method defines a kick behavior from Liu Kahn.
     * 
     * @return damage of the kick
     */
    public int launchKick(){
        System.out.println("Sonia has been launched a kick.");
        this.powerAcum += 15;
        return kickDamage;
    }

    public int launchPunch(){
        System.out.println("Sonia has been launched a punch.");
        this.powerAcum += 15;
        return this.punchDamage;
    }

    /**
     * This method launch a power to the oponent.
     */
    public boolean launchPower(){
        if(this.powerAcum >= 100){
            this.powerAcum = 0;
            return true;
        }
        return false;
    }

    /**
     * This method checks if the power is ready to be launched.
     * @return true if power is ready
     */
    public boolean isPowerReady(){
        return this.powerAcum >= 100? true : false;
    }
}