import java.io.Serializable;

public class Student implements Serializable {

    private static final long serialVersionUID = 1L;

    private String name;
    private int code;
    private String email;

    public Student(String name, int code, String email){
        this.name = name;
        this.code = code;
        this.email = email;
    }

    public String getName() {
        return name;
    }


    public void setName(String name) {
        this.name = name;
    }

    public int getCode() {
        return code;
    }


    public void setCode(int code) {
        this.code = code;
    }

    public String getEmail() {
        return email;
    }


    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString(){
        return "I am a student. My name is " + this.name +
                ", my code is " + this.code + ", and my email is " +
                this.email;
    }
}