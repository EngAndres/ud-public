import java.io.*;

public class App {
    
    public static void serializeStudent(Student student, String filename){
        try(FileOutputStream fileOut = new FileOutputStream(filename);
            ObjectOutputStream out = new ObjectOutputStream(fileOut)){

            out.writeObject(student);

        } catch(IOException e){
            System.out.println("Serialization failed.");
        }
    }

    public static Student deserializeStudent(String filename){
        try(FileInputStream fileIn = new FileInputStream(filename);
            ObjectInputStream in = new ObjectInputStream(fileIn)) {
            Student student = (Student) in.readObject();
            return student;
        } catch (IOException | ClassNotFoundException e) {
            System.out.println("Deserialization failed.");
            return null;
        }
    }
    
    public static void main(String[] args) throws Exception {
        Student s = new Student("Pepita", 1234, "pepita@ud.edu.co", "admin123");
        System.out.println("First:" + s);

        String currentDir = System.getProperty("user.dir");
        String filename = currentDir + "/student.ud";

        serializeStudent(s, filename);
        Student s2 = deserializeStudent(filename);

        System.out.println("Second: " + s2);
    }
}
