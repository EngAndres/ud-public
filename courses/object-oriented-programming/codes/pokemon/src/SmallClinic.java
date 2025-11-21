/*
 * 
 */

/**
 * 
 */ 
public class SmallClinic implements IClinic {

    public String nurse;

    public SmallClinic(String nurseName){
        this.nurse = nurseName;
    }

    @Override
    public void recovery(Pokemon pokemon) {
        pokemon.healthRecovery();
    }
    
}
