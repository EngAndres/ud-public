/*
 * This is a class to handle web services
 * related to user functionalities.
 * 
 * Author: Carlos Andres Sierra <casierrav@udistrital.edu.co>
 */

package com.example.condor.controllers;

import java.util.Optional;
import com.example.condor.data_objects.UserData;
import com.example.condor.data_objects.AuthData;
import com.example.condor.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/users")
public class UserController {
    
    @Autowired
    private UserService userServices;

    /**
     * This service is used to get a user by the id.
     * @param id
     * @return user information
     */
    @GetMapping("/by_id/{idUser}")
    public Optional<UserData> getUserById(@PathVariable("idUser") Integer id){
        return userServices.getUserById(id);
    }

    /**
     * This service is used to authenticate an user in the application. 
     * @param authData
     * @return An object with user data if it is authenticated.
     */
    @PostMapping("/auth")
    public Optional<UserData> authUser(@RequestBody AuthData authData){
        return userServices.authUser(authData);
    }

    /**
     * This service is used to add a new user in the application.
     * @param userData
     * @return An object with user data.
     */
    @PostMapping("/addUser")
    @ResponseStatus(HttpStatus.CREATED)
    public UserData createUser(@RequestBody UserData userData){
        return userServices.addUser(userData);
    }
}
