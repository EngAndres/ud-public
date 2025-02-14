/**
 * This file has a class to define a DTO to move information
 * required for authentication.
 * 
 * Author: Carlos Andres Sierra <cavirguezs@udistrital.edu.co>
 */

package com.ud.machines.data_objects;

 /**
  * This class is used to move information required for authentication.
  */
public class AuthData {

    private String username;
    private String password;

    public AuthData(String username, String password){
        this.username = username;
        this.password = password;
    }

    public String getUsername(){
        return this.username;
    }

    public String getPassword(){
        return this.password;
    }
}
