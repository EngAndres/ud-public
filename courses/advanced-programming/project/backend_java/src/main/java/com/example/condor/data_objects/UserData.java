/**
 * This file has a class to define a DAO to handle
 * user information data structure.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

package com.example.condor.data_objects;

 /**
  * This class is used to define a DAO to handle user information data structure.
  */
public class UserData {

    public int id;
    public String name;
    public String username;
    public String password;
    public String language;
    public String location;
    public int age;

    public UserData(int id, String name, String username, String password, String language, String location, int age){
        this.id = id;
        this.name = name;
        this.username = username;
        this.password = password;
        this.language = language;
        this.location = location;
        this.age = age;
    }
}
