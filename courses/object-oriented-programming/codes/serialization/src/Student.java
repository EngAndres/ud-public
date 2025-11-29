import java.io.Serializable;
import java.util.Base64;
public class Student implements Serializable {

    private static final long serialVersionUID = 1L;

    private String name;
    private int code;
    private String email;
    private String password_;

    public Student(String name, int code, String email, String password){
        this.name = name;
        this.code = code;
        this.email = email;
        this.password_ = encrypt(password);
    }

    private String encrypt(String password){
        return Base64.getEncoder().encodeToString(password.getBytes());
    }

    public String decrypt(){
        return new String(Base64.getDecoder().decode(this.password_));
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
                this.email + " with "+ password_ + "(" + decrypt() +")";
    }
}