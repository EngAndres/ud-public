public abstract class MotherCell(){

    protected String code = "accgtcg";
    protected String activation = "" 

    public MotherCell(String activation){
        this.activation = activation;
    }

    public MotherCell clone() {
        return new MotherCell(this.activation)
    }

    public String toString(){
        return "Code: " + this.code + "\tActivation: " + this.activation;
    }
}