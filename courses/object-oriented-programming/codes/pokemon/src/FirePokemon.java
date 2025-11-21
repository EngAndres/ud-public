/*
 * 
 */

 /**
  * 
  */
public class FirePokemon extends Pokemon {

    public FirePokemon(int attackDamage, int baseDefense){
        super(attackDamage, baseDefense);
    }

    @Override
    public int attack() {
        return this.attackDamage * this.health;
    }


    @Override
    public void defense(String typeAdversary, int attackValue) {
        if(typeAdversary.equals("water")){
            this.health -= attackValue;
        } else {
            double currentDefense = (this.baseDefense * this.health) / 100.0;
            double damage = attackValue - currentDefense;
            this.health -= damage > 0? damage : Math.abs(damage) * 0.1;
        }
    }

    @Override
    public void healthRecovery() {
        int healthUnit = 2;
        this.health += this.health == 100? 0 : healthUnit;
    }
}