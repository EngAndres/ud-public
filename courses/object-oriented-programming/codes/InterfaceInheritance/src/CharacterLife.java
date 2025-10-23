public class CharacterLife {
    private int life;

    public CharacterLife(){
        this.life = 100;
    }

    public void sufferDamage(int damage){
        this.life -= damage;
    }

    public boolean isDead(){
        return this.life < 0 ? true : false;
    }
}
