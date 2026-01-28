package main.java.com.ud.oop.final_project.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Person {

    @JsonProperty("id")
    private Integer id;
    
    @JsonProperty("name")
    private String name;

    @JsonProperty("email")
    private String email;

    public Person(Integer id, String name, String email){
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
