public class Kitana extends CharacterLife implements MortalKombatCharacter{

    public Kitana(){}

    public int launchKick(){
        System.out.println("Kitana has launched a kick.");
        return 15;
    }

    public int launchPunch(){
        System.out.println("Kitana has launched a punch");
        return 5;
    }

    public boolean launchPower(){
        return false;
    }

}