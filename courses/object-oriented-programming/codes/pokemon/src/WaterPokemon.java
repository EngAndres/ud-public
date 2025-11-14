public class WaterPokemon extends PokemonFeatures implements Pokemon {

    public WaterPokemon(int attackDamage, int baseDefense){
        super(attackDamage, baseDefense);
    }

    @Override
    public int attack() {
        return (this.attackDamage * this.health) / 100;
    }

    @Override
    public Pokemon evolute() {
        return null;
    }

    @Override
    public void defense(String typeAdversary, int attackValue) {
        if(typeAdversary.equals("electric")){
            this.health -= attackValue * 1.5;
        } else {
            this.health -= attackValue;
        }
    }

    @Override
    public void healthRecovery() {
        this.health += 3;
        if(this.health > 100)
            this.health = 100;
    }
    
}
