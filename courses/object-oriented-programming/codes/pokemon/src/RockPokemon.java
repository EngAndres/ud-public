public class RockPokemon extends Pokemon {

    public RockPokemon(int attackDamage, int baseDefense){
        super(attackDamage, baseDefense);
    }

    @Override
    public int attack() {
        return this.attackDamage;
    }

    @Override
    public void defense(String typeAdversary, int attackValue) {
        this.health -= attackValue;
    }

    @Override
    public void healthRecovery() {
        this.health += (int)((5 * this.health) / 100.0);
    }
}