public abstract class Pokemon {

    protected int attackDamage;
    protected int baseDefense;
    protected int health;
    
    protected Pokemon(int attackDamage, int baseDefense){
        this.attackDamage = attackDamage;
        this.baseDefense = baseDefense;
        this.health = 100;
    }

    public boolean isDefeated(){
        int minimumLevel = 5;
        return this.health < minimumLevel;
    }
    
    public abstract int attack();

    public Pokemon evolute(){
        return null;
    }

    public abstract void defense(String typeAdversary, int attackValue);

    public abstract void healthRecovery();
}