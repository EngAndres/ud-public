package main.java.com.ud.oop.final_project;

import main.java.com.ud.oop.final_project.model.Person;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.TypeReference;
import java.io.File;

import java.util.List;
import java.util.ArrayList;

public class JSONManager {
    private final ObjectMapper objectMapper;
    private final String filePath;

    public JSONManager(String filePath){
        this.filePath = filePath;
        this.objectMapper = new ObjectMapper();
    }

    // One only object
    public void writePersonToFile(Person person){
        try{
            this.objectMapper.writeValue(new File(this.filePath), person);
        } catch(Exception e){
            System.out.println("Cannot save the object.");
        }
    }

    // only one object
    public Person readPersonFromFile(){
        if(this.isFile()) {
            File file = new File(this.filePath);
            return this.objectMapper.readValue(file, Person.class);
        } else {
            System.out.println("File does not exist.");
        }
    }
    
    private void writePersonListToFile(List<Person> persons){
        try{
            this.objectMapper.writeValue(new File(this.filePath), persons);
        } catch(Exception e){}
    }

    private List<Person> readPersonListFromFile(){
        try{
            if(this.isFile()){
                File file = new File(this.filePath);
                TypeReference<List<Person>> tr = new TypeReference<List<Person>>();
                return this.objectMapper.readValue(file, tr);
            } else {
                return new ArrayList<Person>();
            }
        } catch(Exception e) {}
    }

    public void addPersonToFile(Person person){
        List<Person> persons = this.readPersonListFromFile();
        persons.add(person);
        this.writePersonListToFile(persons);
    }

    public Person findPersonById(Integer idForSearch){
        List<Person> persons = this.readPersonListFromFile();
        return persons.stream()
                .filter(person -> person.getId().equals(idForSearch))
                .findFirst()
                .orElse(null);
    }

    public Person findPersonByEmail(String email){
        List<Person> persons = this.readPersonListFromFile();
        return persons.stream()
                .filter(person -> person.getEmail().equals(email))
                .findFirst()
                .orElse(null);
    }

    public boolean deletePersonFromFile(Integer idForSearch){
        List<Person> persons = this.readPersonListFromFile();
        for(Person p: persons){
            if(p.getId().equals(idForSearch)){
                persons.remove(p);
                break;
            }
        }
        this.writePersonListToFile(persons);
    }

    private boolean isFile(){
        return new File(this.filePath).exists();
    }
}
