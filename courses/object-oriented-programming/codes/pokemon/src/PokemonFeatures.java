public class PokemonFeatures {
    
    protected int attackDamage;
    protected int baseDefense;
    protected int health;
    
    public PokemonFeatures(int attackDamage, int baseDefense){
        this.attackDamage = attackDamage;
        this.baseDefense = baseDefense;
        this.health = 100;
    }

    public boolean isDefeated(){
        int minimumLevel = 5;
        return this.health < minimumLevel;
    }
}