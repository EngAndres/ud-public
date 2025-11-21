/*
 * 
 */

 /**
  * 
  */
public class BigClinic implements IClinic {

    public String medicalDoctor;

    public BigClinic(String medicalDoctorName){
        this.medicalDoctor = medicalDoctorName;
    }

    @Override
    public void recovery(Pokemon pokemon) {
        pokemon.healthRecovery();
        pokemon.healthRecovery();
    }
}