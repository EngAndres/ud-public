/*
 * 
 */

 /**
  * 
  */
public class ElectricPokemon extends  Pokemon {

    public ElectricPokemon(int attackDamage, int baseDefense){
        super(attackDamage, baseDefense);
    }

    @Override
    public int attack() {
        return this.attackDamage;
    }

    @Override
    public void defense(String typeAdversary, int attackValue) {
        if(typeAdversary.equals("rock")){
            this.health -= attackValue * 1.1;
        } else if(typeAdversary.equals("water")){
            this.health -= attackValue * 0.8;
        } else {
            this.health -= attackValue;
        }
    }

    @Override
    public void healthRecovery() {
        this.health += 5;
        if(this.health > 100)
            this.health = 100;
    }
}