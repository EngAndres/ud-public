package example_encapsulation;
public class Student {
    private double grade;
    private int age;
    public String name;

    // Constructor
    public Student(String name, double grade, int age){
        //this.grade = grade; OLD
        this.setGrade(grade); // NEW
        this.name = name;
        //this.age = age;
        this.setAge(age);
    }

    // Method
    /**
     * This method returns a current state about
     * student perception of its performance.
     * @return string with the state
     */
    public String comoVoy(){
        if(grade >= 4.0){
            return "Vamos melo!";
        }
        else if(grade >= 3.0){
            return "Andando";
        }
        else {
            return "Ahi llevandola";
        }
    }

    public void setGrade(double newGrade){
        if(newGrade >= 0.0 && newGrade <= 5.0) {
            this.grade = newGrade;
        }
        else{
            System.out.println("Valor incorrecto de nota.");
        }
    }

    protected double getGrade(){
        return this.grade;
    }

    public void setAge(int newAge){
        if(newAge >= 0){
            this.age = newAge;
        }
        else{
            System.out.println("La edad no debería ser negativa.");
        }
    }

    public int getAge(){
        // validate if current user has grants
        return this.age;
    }

    
}
