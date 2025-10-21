public class LiuKahn implements MortalKombatCharacter {

    private int kickDamage;
    private int punchDamage;
    private int powerAcum;

    public LiuKahn(int kickDamage, int punchDamage){
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
        System.out.println("Liu has been launched a kick. Damage: " + this.kickDamage);
        this.powerAcum += 20;
        return kickDamage;
    }

    public int launchPunch(){
        System.out.println("Liu has been launched a punch. Damage: " + this.punchDamage);
        this.powerAcum += 15;
        return this.punchDamage;
    }

    public boolean launchPower(){
        if(this.powerAcum >= 100){
            this.powerAcum = 0;
            return true;
        }
        return false;
    }
}
